# server/app/services/qa_indexing_service.py
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.question import Question
from app.models.answer import Answer
from app.infra.embeddings import generate_embeddings
from app.services.answer_service import AnswerService


class QAIndexingService:
    """Service to index Q&A data into the vector store for RAG retrieval."""
    
    def __init__(self, db: Session, collection, embedding_model):
        self.db = db
        self.collection = collection
        self.embedding_model = embedding_model
        self._answer_service = AnswerService(db)  # For computing vote scores
    
    def _safe_delete(self, ids: List[str]) -> None:
        """Safely delete entries, ignoring errors if they don't exist."""
        if not ids:
            return
        try:
            self.collection.delete(ids=ids)
        except Exception as e:
            # entry might not exist, which is fine
            pass
    
    def _get_answer_vote_score(self, answer_id: int) -> int:
        """Get vote score for an answer, with error handling."""
        try:
            return self._answer_service.get_answer_vote_score(answer_id)
        except Exception as e:
            print(f"Error getting vote score for answer {answer_id}: {e}")
            return 0
    
    def index_question_with_answers(self, question: Question) -> None:
        """
        Index a question together with ALL its current answers as a single chunk.
        This method ensures no duplicates by always removing old entries first.
        """
        try:
            # Always fetch fresh answers from DB
            # Order by accepted status first, then by creation date (can't order by vote_score directly)
            answers = self.db.query(Answer).filter(
                Answer.question_id == question.id
            ).order_by(Answer.is_accepted.desc(), Answer.created_at.asc()).all()
            
            # Calculate vote scores for each answer and sort by score (in Python)
            answers_with_scores = []
            for answer in answers:
                try:
                    vote_score = self._get_answer_vote_score(answer.id)
                    answers_with_scores.append((answer, vote_score))
                except Exception as e:
                    print(f"Error getting vote score for answer {answer.id}: {e}")
                    answers_with_scores.append((answer, 0))
            
            # Sort by accepted status, then by vote score (descending)
            answers_with_scores.sort(key=lambda x: (x[0].is_accepted, x[1]), reverse=True)
            answers = [ans for ans, _ in answers_with_scores]
            
            # Build combined text
            qa_text_parts = [
                f"Question: {question.title}",
                f"Details: {question.content}",
            ]
            
            if answers:
                qa_text_parts.append("\nAnswers:")
                for idx, answer in enumerate(answers, 1):
                    try:
                        accepted_marker = "✓ (Accepted)" if answer.is_accepted else ""
                        # Get vote score safely
                        vote_score = self._get_answer_vote_score(answer.id)
                        vote_info = f" (Score: {vote_score})" if vote_score > 0 else ""
                        qa_text_parts.append(
                            f"\nAnswer {idx} {accepted_marker}{vote_info}:\n{answer.content}"
                        )
                    except Exception as e:
                        print(f"Error processing answer {answer.id}: {e}")
                        # Still include the answer, just without vote info
                        qa_text_parts.append(
                            f"\nAnswer {idx}:\n{answer.content}"
                        )
            else:
                qa_text_parts.append("\n(No answers yet)")
            
            qa_text = "\n".join(qa_text_parts)
            
            # Metadata
            qa_metadata = {
                "source": f"qa/question/{question.id}",
                "type": "qa_pair",
                "question_id": str(question.id),
                "author_id": str(question.author_id),
                "created_at": question.created_at.isoformat() if hasattr(question.created_at, 'isoformat') else str(question.created_at),
                "is_solved": str(question.is_solved),
                "answer_count": str(len(answers)),
                "has_accepted_answer": str(any(a.is_accepted for a in answers)),
                "indexed_at": datetime.now(timezone.utc).isoformat(),
            }
            
            # Generate embedding
            embedding = generate_embeddings([qa_text], self.embedding_model)[0]
            
            # Remove old entries
            question_id = question.id
            ids_to_remove = [
                f"qa_combined_{question_id}",
                f"qa_question_{question_id}",
            ]
            
            # Also remove any individual answer entries for this question
            answer_ids = [f"qa_answer_{answer.id}" for answer in answers]
            ids_to_remove.extend(answer_ids)
            
            # Remove old entries
            self._safe_delete(ids_to_remove)
            
            # Add the combined entry
            combined_id = f"qa_combined_{question_id}"
            self.collection.add(
                ids=[combined_id],
                embeddings=[embedding],
                documents=[qa_text],
                metadatas=[qa_metadata],
            )
            
            print(f"Successfully indexed question {question.id} with {len(answers)} answer(s)")
            
        except Exception as e:
            print(f"Error in index_question_with_answers for question {question.id}: {e}")
            import traceback
            traceback.print_exc()
            raise  # Re-raise so the route handler knows it failed
    
    def index_question(self, question: Question) -> None:
        """
        Index only the question (for when there are no answers yet).
        """
        try:
            question_text = f"Question: {question.title}\n\n{question.content}"
            question_metadata = {
                "source": f"qa/question/{question.id}",
                "type": "question",
                "question_id": str(question.id),
                "author_id": str(question.author_id),
                "created_at": question.created_at.isoformat() if hasattr(question.created_at, 'isoformat') else str(question.created_at),
                "is_solved": str(question.is_solved),
                "answer_count": "0",
                "indexed_at": datetime.now(timezone.utc).isoformat(),
            }
            
            # Generate embedding
            embedding = generate_embeddings([question_text], self.embedding_model)[0]
            
            question_id = question.id
            question_only_id = f"qa_question_{question_id}"
            
            # Remove any existing entries
            self._safe_delete([
                f"qa_combined_{question_id}",
                question_only_id,
            ])
            
            # Add question-only entry
            self.collection.add(
                ids=[question_only_id],
                embeddings=[embedding],
                documents=[question_text],
                metadatas=[question_metadata],
            )
            
            print(f"Successfully indexed question {question.id} (no answers yet)")
            
        except Exception as e:
            print(f"Error indexing question {question.id}: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def index_answer(self, answer: Answer) -> None:
        """
        Index an answer by re-indexing the entire Q&A pair.
        """
        try:
            # Force session to see latest committed data
            self.db.expire_all()
            
            question = self.db.query(Question).filter(Question.id == answer.question_id).first()
            if not question:
                print(f"Warning: Question {answer.question_id} not found when indexing answer {answer.id}")
                return
            
            # Re-index the whole Q&A pair
            self.index_question_with_answers(question)
            
        except Exception as e:
            print(f"Error indexing answer {answer.id}: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def reindex_question_with_answers(self, question_id: int) -> None:
        """Re-index a question and all its answers."""
        try:
            question = self.db.query(Question).filter(Question.id == question_id).first()
            if not question:
                print(f"Warning: Question {question_id} not found for re-indexing")
                return
            
            self.index_question_with_answers(question)
        except Exception as e:
            print(f"Error re-indexing question {question_id}: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def remove_question(self, question_id: int) -> None:
        """Remove a question and its answers from the vector store."""
        try:
            # Get all answer IDs first
            answers = self.db.query(Answer).filter(Answer.question_id == question_id).all()
            answer_ids = [f"qa_answer_{answer.id}" for answer in answers]
            
            # Remove all entries
            ids_to_remove = [
                f"qa_combined_{question_id}",
                f"qa_question_{question_id}",
            ] + answer_ids
            
            self._safe_delete(ids_to_remove)
            print(f"Removed question {question_id} from vector store")
        except Exception as e:
            print(f"Error removing question {question_id}: {e}")
            import traceback
            traceback.print_exc()
    
    def remove_answer(self, answer_id: int) -> None:
        """Remove an answer and re-index the question with remaining answers."""
        try:
            answer = self.db.query(Answer).filter(Answer.id == answer_id).first()
            if not answer:
                print(f"Warning: Answer {answer_id} not found for removal")
                return
            
            question_id = answer.question_id
            
            # Re-index the question with remaining answers
            question = self.db.query(Question).filter(Question.id == question_id).first()
            if question:
                self.index_question_with_answers(question)
        except Exception as e:
            print(f"Error removing answer {answer_id}: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def update_answer_metadata(self, answer: Answer) -> None:
        """Re-index when answer metadata changes."""
        try:
            question = self.db.query(Question).filter(Question.id == answer.question_id).first()
            if question:
                self.index_question_with_answers(question)
        except Exception as e:
            print(f"Error updating answer metadata for answer {answer.id}: {e}")
            import traceback
            traceback.print_exc()
            raise