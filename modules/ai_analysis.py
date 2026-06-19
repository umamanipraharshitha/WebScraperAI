import os
from google import genai
from google.genai import types

class GeminiAnalyst:
    def __init__(self):
        """Initializes the unified Google GenAI client."""
        # Authenticates seamlessly via the GEMINI_API_KEY environment variable
        self.client = genai.Client()
        self.model = "gemini-2.5-flash" # High speed, optimized for quick context parsing

    def _chunk_text(self, text: str, max_chars: int = 6000) -> list:
        """Splits text into manageable, overlapping structural chunks."""
        if not text:
            return []
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0

        for word in words:
            current_chunk.append(word)
            current_length += len(word) + 1  # accounts for space
            
            if current_length >= max_chars:
                chunks.append(" ".join(current_chunk))
                # Keep an overlap of the last 50 words for context continuity
                current_chunk = current_chunk[-50:]
                current_length = sum(len(w) + 1 for w in current_chunk)

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    def summarize_content(self, raw_text: str) -> str:
        """
        Chunks the text context, minimizes token usage via an intermediate map step,
        and generates a highly dense master corporate summary.
        """
        if not raw_text:
            return "No raw material provided to summarize."

        # Step 1: Chunk the text
        chunks = self._chunk_text(raw_text, max_chars=8000)
        
        # If the text is short, don't waste tokens on a multi-stage summary
        if len(chunks) <= 1:
            return self._generate_final_summary(raw_text)

        # Step 2: Intermediate compression map step (reduces token load for final processing)
        print(f"   [AI Content split into {len(chunks)} chunks for token minimization...]")
        intermediate_summaries = []
        
        for i, chunk in enumerate(chunks, 1):
            map_prompt = (
                "Extract only the key facts, numbers, names, and major core concepts "
                "from this raw text segment. Be incredibly brief and avoid full filler sentences:\n\n"
                f"SEGMENT:\n{chunk}"
            )
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=map_prompt
                )
                if response.text:
                    intermediate_summaries.append(response.text)
            except Exception as e:
                print(f"   ⚠️ Warning skipping sub-chunk {i}: {e}")

        # Step 3: Reduce step (Combine mini summaries into the dense final result)
        combined_context = "\n\n".join(intermediate_summaries)
        return self._generate_final_summary(combined_context)

    def _generate_final_summary(self, condensed_context: str) -> str:
        """Final clean summary step."""
        reduce_prompt = (
            "You are a highly efficient, token-saving analyst. Write an extremely dense, "
            "concise summary of the following data points. Do not waste space on meta-commentary "
            "like 'This text discusses...'. Structure your response exactly as follows:\n\n"
            "## Executive Summary\n(Maximum 4 concise lines)\n\n"
            "## Key Takeaways\n(3-5 high-impact bullet points containing metrics/facts)\n\n"
            "## Recommendations\n(2-3 actionable insights)\n\n"
            f"DATA:\n{condensed_context}"
        )
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=reduce_prompt
            )
            return response.text if response.text else "API returned an empty text layer."
        except Exception as e:
            return f"⚠️ Gemini final processing error: {e}"

# Backwards compatible function layer for main.py integration
def analyze_text_with_gemini(text: str, system_hint: str = "") -> str:
    analyst = GeminiAnalyst()
    return analyst.summarize_content(text)