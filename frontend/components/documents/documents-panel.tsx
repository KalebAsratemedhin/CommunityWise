'use client';

import { useState } from 'react';
import {
  useListDocumentsQuery,
  useUploadDocumentMutation,
  useIndexDocumentMutation,
  useListIndexedDocumentsQuery,
  useDeleteIndexedDocumentMutation,
  type DocumentInfo,
  type IndexedDocumentInfo,
} from '@/lib/api';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Loader2, FileText } from 'lucide-react';

export function DocumentsPanel() {
  const {
    data: documents,
    isLoading: isLoadingDocuments,
    refetch: refetchDocuments,
  } = useListDocumentsQuery();

  const [uploadDocument, { isLoading: isUploading }] =
    useUploadDocumentMutation();
  const [indexDocument, { isLoading: isIndexing }] =
    useIndexDocumentMutation();

  const {
    data: indexedDocuments,
    isLoading: isLoadingIndexed,
    refetch: refetchIndexed,
  } = useListIndexedDocumentsQuery();
  const [deleteIndexedDocument, { isLoading: isDeletingIndexed }] =
    useDeleteIndexedDocumentMutation();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [indexingKey, setIndexingKey] = useState<string | null>(null);

  return (
    <div className="hidden lg:flex h-full w-80 border-l flex-col pt-6 pb-0 pl-4 min-h-0 pr-4">
      <h2 className="text-sm font-semibold mb-3">Documents</h2>

      {/* Upload */}
      <div className="mb-4 space-y-2">
        <label className="text-xs text-muted-foreground">
          Upload document (txt, md, pdf)
        </label>
        <input
          type="file"
          accept=".txt,.md,.pdf"
          onChange={(e) => {
            const file = e.target.files?.[0] ?? null;
            setSelectedFile(file);
          }}
          className="block w-full text-xs text-muted-foreground file:mr-3 file:py-1.5 file:px-3 file:rounded file:border file:border-border file:text-xs file:bg-background file:text-foreground file:cursor-pointer"
        />
        <Button
          size="sm"
          className="w-full"
          disabled={!selectedFile || isUploading}
          onClick={async () => {
            if (!selectedFile) return;
            try {
              await uploadDocument(selectedFile).unwrap();
              setSelectedFile(null);
              await refetchDocuments();
            } catch (err) {
              console.error('Upload failed', err);
            }
          }}
        >
          {isUploading ? (
            <span className="flex items-center gap-2">
              <Loader2 className="w-3 h-3 animate-spin" /> Uploading...
            </span>
          ) : (
            'Upload'
          )}
        </Button>
      </div>

      {/* Lists: uploaded + indexed, scroll together */}
      <ScrollArea className="flex-1 pr-2">
        <div className="flex flex-col gap-4">
          {/* Uploaded files */}
          <div className="flex flex-col">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-muted-foreground">
                Uploaded files
              </span>
              <Button
                size="icon"
                variant="ghost"
                className="h-6 w-6"
                onClick={() => refetchDocuments()}
                disabled={isLoadingDocuments}
                aria-label="Refresh uploaded documents"
              >
                <Loader2
                  className={`w-3 h-3 ${
                    isLoadingDocuments ? 'animate-spin' : ''
                  }`}
                />
              </Button>
            </div>

            <div className="space-y-2">
              {documents && documents.length > 0 ? (
                documents
                  .filter(
                    (doc: DocumentInfo) =>
                      !(
                        doc.key.endsWith('/') &&
                        (!doc.size || Number(doc.size) === 0)
                      ),
                  )
                  .map((doc: DocumentInfo) => {
                    const displayName =
                      doc.original_filename ||
                      doc.key.replace(/^uploads\//, '');
                    const extMatch = displayName.match(/\.([a-zA-Z0-9]+)$/);
                    const ext = extMatch ? extMatch[1].toLowerCase() : '';
                    const label =
                      ext === 'pdf'
                        ? 'PDF'
                        : ext === 'txt'
                        ? 'Text'
                        : ext === 'md'
                        ? 'Markdown'
                        : ext
                        ? ext.toUpperCase()
                        : 'File';

                    return (
                      <div
                        key={doc.key}
                        className="border rounded-md px-2 py-2 text-xs space-y-1"
                      >
                        <div className="flex items-start gap-2">
                          <div className="mt-0.5 flex h-6 w-6 items-center justify-center rounded bg-muted">
                            <FileText className="h-3.5 w-3.5 text-muted-foreground" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center justify-between gap-2">
                              <div className="flex-1 text-left break-words">
                                <div className="font-medium leading-snug">
                                  {doc.signed_url ? (
                                    <button
                                      type="button"
                                      className="text-left underline-offset-2 hover:underline"
                                      onClick={() => {
                                        window.open(doc.signed_url!, '_blank');
                                      }}
                                    >
                                      {displayName}
                                    </button>
                                  ) : (
                                    displayName
                                  )}
                                </div>
                              </div>
                              <span className="ml-2 inline-flex items-center rounded-full bg-muted px-2 py-0.5 text-[10px] font-medium text-muted-foreground shrink-0">
                                {label}
                              </span>
                            </div>
                          </div>
                        </div>
                        <div className="text-[10px] text-muted-foreground flex justify-between">
                          <span>
                            {doc.size !== undefined
                              ? `${(Number(doc.size) / 1024).toFixed(1)} KB`
                              : '—'}
                          </span>
                          <span>
                            {doc.last_modified
                              ? new Date(doc.last_modified).toLocaleString()
                              : ''}
                          </span>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          className="mt-2 w-full justify-center rounded-md border-dashed"
                          disabled={isIndexing && indexingKey === doc.key}
                          onClick={async () => {
                            try {
                              setIndexingKey(doc.key);
                              await indexDocument({
                                s3_key: doc.key,
                                filename: undefined,
                              }).unwrap();
                              await refetchIndexed();
                            } catch (err) {
                              console.error('Indexing failed', err);
                            } finally {
                              setIndexingKey(null);
                            }
                          }}
                        >
                          {isIndexing && indexingKey === doc.key ? (
                            <span className="flex items-center gap-2 text-xs font-medium">
                              <Loader2 className="w-3 h-3 animate-spin" />
                              Indexing document...
                            </span>
                          ) : (
                            <span className="flex items-center gap-2 text-xs font-medium">
                              Index document
                            </span>
                          )}
                        </Button>
                      </div>
                    );
                  })
              ) : (
                <p className="text-[11px] text-muted-foreground">
                  No documents uploaded yet.
                </p>
              )}
            </div>
          </div>

          {/* Indexed documents */}
          <div className="flex flex-col border-t pt-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-muted-foreground">
                Indexed documents
              </span>
              <Button
                size="icon"
                variant="ghost"
                className="h-6 w-6"
                onClick={() => refetchIndexed()}
                disabled={isLoadingIndexed}
                aria-label="Refresh indexed documents"
              >
                <Loader2
                  className={`w-3 h-3 ${
                    isLoadingIndexed ? 'animate-spin' : ''
                  }`}
                />
              </Button>
            </div>

            <div className="space-y-2">
              {indexedDocuments && indexedDocuments.length > 0 ? (
                indexedDocuments.map((doc: IndexedDocumentInfo) => (
                  <div
                    key={doc.source}
                    className="border rounded-md px-2 py-2 text-xs space-y-1"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex-1 break-words font-medium leading-snug">
                        {doc.source}
                      </div>
                      <span className="text-[10px] text-muted-foreground">
                        {doc.chunks_count} chunks
                      </span>
                    </div>
                    <div className="text-[10px] text-muted-foreground flex justify-between">
                      <span>
                        {doc.last_indexed_at
                          ? new Date(doc.last_indexed_at).toLocaleString()
                          : 'Time unknown'}
                      </span>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      className="mt-2 w-full justify-center rounded-md border border-destructive/50 text-destructive hover:bg-destructive/5"
                      disabled={isDeletingIndexed}
                      onClick={async () => {
                        try {
                          await deleteIndexedDocument(doc.source).unwrap();
                          await refetchIndexed();
                        } catch (err) {
                          console.error(
                            'Failed to delete indexed document',
                            err,
                          );
                        }
                      }}
                    >
                      {isDeletingIndexed ? (
                        <span className="flex items-center gap-2 text-xs font-medium">
                          <Loader2 className="w-3 h-3 animate-spin" />
                          Removing from index...
                        </span>
                      ) : (
                        <span className="flex items-center gap-2 text-xs font-medium">
                          Remove from index
                        </span>
                      )}
                    </Button>
                  </div>
                ))
              ) : (
                <p className="text-[11px] text-muted-foreground">
                  No documents indexed yet.
                </p>
              )}
            </div>
          </div>
        </div>
      </ScrollArea>
    </div>
  );
}


