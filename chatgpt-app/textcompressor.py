import json


class TextCompressor:

    def __init__(self):
        # Dictionary to store tokens and their corresponding IDs
        self.token2id = {}
        # Dictionary to store IDs and their corresponding tokens
        self.id2token = {}
        # Next available ID for a new token
        self.next_id = 0

    def tokenize(self, text):
        """Tokenizes the text into words."""
        return text.split()

    def compress(self, text):
        """Compresses the text into a sequence of token IDs."""
        tokens = self.tokenize(text)
        compressed_text = []

        for token in tokens:
            # If token is not in the dictionary, add it
            if token not in self.token2id:
                self.token2id[token] = self.next_id
                self.id2token[self.next_id] = token
                self.next_id += 1

            compressed_text.append(self.token2id[token])

        return compressed_text

    def decompress(self, compressed_text):
        """Decompresses the sequence of token IDs back into the original text."""
        return ' '.join([self.id2token[token_id] for token_id in compressed_text])

class CodeTextCompressor(TextCompressor):

    def tokenize(self, text):
        """Tokenizes the code into words and symbols."""
        tokens = []
        token = ""
        for char in text:
            if char.isalnum() or char == '_':
                token += char
            else:
                if token:
                    tokens.append(token)
                    token = ""
                tokens.append(char)

        # Append the last token if it exists
        if token:
            tokens.append(token)

        return tokens

    def compare_lengths(self, original_text, prompt):
        """Compares the length of the original text with the length of the prompt."""

        original_length = len(original_text)
        prompt_length = len(prompt)
        return original_length, prompt_length


    def generate_prompt(self, text):
        """Generates a more compact prompt with the dictionary and compressed text."""

        # Convert dictionary to a JSON string without spaces for compactness
        dict_str = json.dumps(self.token2id, separators=(',', ':'))

        prompt = f"Here is dict {dict_str}, " \
                 f"use dict to decode this compressed text {self.compress(text)}"

        return prompt


# Test the system
if __name__ == '__main__':
    text = "Hello, how are you? Hello, I am good."

    compressor = TextCompressor()
    compressed_text = compressor.compress(text)
    decompressed_text = compressor.decompress(compressed_text)

    compressed_text, decompressed_text
