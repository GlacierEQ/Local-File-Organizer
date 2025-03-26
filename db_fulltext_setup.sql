-- Add full-text search column and index
ALTER TABLE documents ADD COLUMN search_vector tsvector;
UPDATE documents SET search_vector = to_tsvector('english', content);
CREATE INDEX search_idx ON documents USING gin(search_vector);
-- Example query provided in comments.
-- SELECT filename, ts_rank(search_vector, to_tsquery('english', 'AI & legal')) AS rank
-- FROM documents
-- WHERE search_vector @@ to_tsquery('english', 'AI & legal')
-- ORDER BY rank DESC;
