import unittest
from autogen.agentchat.contrib.rag.encoder import (
    Encoder,
    EmbeddingFunctionFactory,
    SentenceTransformerEmbeddingFunction,
    EmbeddingFunction,
    Document,
    Chunk,
)


class TestEncoder(unittest.TestCase):
    def test_encode_chunks(self):
        encoder = Encoder()
        chunks = [Chunk(content="This is chunk 1"), Chunk(content="This is chunk 2"), Chunk(content="This is chunk 3")]
        documents = encoder.encode_chunks(chunks)
        self.assertEqual(len(documents), len(chunks))
        for document, chunk in zip(documents, chunks):
            self.assertIsInstance(document, Document)
            self.assertEqual(document.content_embedding, encoder.embedding_function(chunk.content)[0])
            self.assertEqual(document.embedding_model, encoder.model_name)
            self.assertEqual(document.dimensions, encoder.dimensions)

    def test_embedding_function_factory(self):
        embedding_function = EmbeddingFunctionFactory.create_embedding_function("sentence_transformer")
        self.assertIsInstance(embedding_function, SentenceTransformerEmbeddingFunction)
        self.assertIsInstance(embedding_function, EmbeddingFunction)

    def test_sentence_transformer_embedding_function(self):
        embedding_function = SentenceTransformerEmbeddingFunction()
        input_text = "This is a test sentence."
        vectors = embedding_function(input_text)
        self.assertIsInstance(vectors, list)


class TestEmbeddingFunction(unittest.TestCase):
    def test_sentence_transformer_embedding_function(self):
        embedding_function = SentenceTransformerEmbeddingFunction()
        vectors = embedding_function("hello")
        self.assertIsInstance(vectors, list)
        self.assertIsInstance(vectors[0], list)


class TestEmbeddingFunctionFactory(unittest.TestCase):
    def test_create_embedding_function(self):
        embedding_function = EmbeddingFunctionFactory.create_embedding_function("sentence_transformer")
        self.assertIsInstance(embedding_function, SentenceTransformerEmbeddingFunction)

    def test_create_embedding_function_invalid(self):
        with self.assertRaises(ValueError):
            EmbeddingFunctionFactory.create_embedding_function("invalid")


if __name__ == "__main__":
    unittest.main()