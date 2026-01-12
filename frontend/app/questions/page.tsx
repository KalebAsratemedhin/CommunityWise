'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import { QuestionCard } from '@/components/questions/question-card';
import { QuestionForm } from '@/components/questions/question-form';
import { useGetQuestionsQuery } from '@/lib/api/questionsApi';
import { AuthGuard } from '@/components/auth/auth-guard';

function QuestionsPage() {
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState<'all' | 'solved' | 'unsolved'>('all');
  const { data: questions, isLoading, refetch } = useGetQuestionsQuery({
    is_solved: filter === 'all' ? undefined : filter === 'solved',
  });

  return (
    <div className="flex flex-col h-screen bg-background">
      <div className="container max-w-4xl mx-auto py-2 px-4">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Questions & Answers</h1>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus className="h-4 w-4 mr-2" />
          Ask Question
        </Button>
      </div>

      {showForm && (
        <div className="mb-6 p-4 border rounded-lg bg-background">
          <QuestionForm
            onSuccess={() => {
              setShowForm(false);
              refetch();
            }}
          />
        </div>
      )}

      <div className="flex gap-2 mb-4">
        <Button
          variant={filter === 'all' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setFilter('all')}
        >
          All
        </Button>
        <Button
          variant={filter === 'unsolved' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setFilter('unsolved')}
        >
          Unanswered
        </Button>
        <Button
          variant={filter === 'solved' ? 'default' : 'outline'}
          size="sm"
          onClick={() => setFilter('solved')}
        >
          Solved
        </Button>
      </div>

      {isLoading ? (
        <div className="text-center py-4 text-muted-foreground">Loading questions...</div>
      ) : questions && questions.length > 0 ? (
        <div className="flex flex-col gap-4">
          {questions.map((question) => (
            <QuestionCard key={question.id} question={question} />
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-muted-foreground">
          No questions yet. Be the first to ask!
        </div>
      )}
    </div>
    </div>
  );
}

export default function ProtectedQuestionsPage() {
  return (
    <AuthGuard>
      <QuestionsPage />
    </AuthGuard>
  );
}