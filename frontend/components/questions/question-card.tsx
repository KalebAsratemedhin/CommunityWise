'use client';

import Link from 'next/link';
import { formatDistanceToNow, parseISO } from 'date-fns';
import { MessageSquare, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { VoteButtons } from '@/components/questions/vote-buttons';
import type { Question } from '@/lib/api/questionsApi';

interface QuestionCardProps {
  question: Question;
}

export function QuestionCard({ question }: QuestionCardProps) {
  return (
    <Link href={`/questions/${question.id}`} className="block">
      <div className="border rounded-lg p-4 hover:bg-accent/50 transition-colors cursor-pointer">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="text-lg font-semibold line-clamp-2">{question.title}</h3>
              {question.is_solved && (
                <CheckCircle2 className="h-5 w-5 text-green-500 shrink-0" />
              )}
            </div>
            <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
              {question.content}
            </p>
            <div className="flex items-center gap-4 text-xs text-muted-foreground">
              <span>
                {formatDistanceToNow(
                typeof question.created_at === 'string' 
                    ? parseISO(question.created_at) 
                    : new Date(question.created_at), 
                { addSuffix: true }
                )}
              </span>
              <div className="flex items-center gap-1">
                <MessageSquare className="h-4 w-4" />
                <span>{question.answer_count} answers</span>
              </div>
            </div>
          </div>
          <VoteButtons
            votableType="question"
            votableId={question.id}
            score={question.vote_score}
            userVote={question.user_vote}
            disabled={false}
          />
        </div>
      </div>
    </Link>
  );
}