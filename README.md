

This project solves the problem of **entity resolution** by identifying and grouping duplicate company records that appear across multiple systems. Using fuzzy string matching and graph clustering, the solution is able to handle slight differences in company names (e.g., "Acme Inc." vs "Acme Incorporated") and assign consistent identifiers.


### What I Focused On:

- **Understanding the real problem:**  
  I didn’t jump straight into code. I thought first about what makes two companies "the same" in practice. It turns out, exact string matching is too brittle. Instead, I needed to build some tolerance into the comparisons.

- **Choosing the right attributes:**  
  Even though there were other fields (like address or phone), many were missing or inconsistent. So I decided to focus just on `company_name` for this solution. In a real-world system, I'd combine multiple signals—but here, simpler was better for showing clear logic.

- **Handling messy or incomplete data:**  
  Not all names were clean or even present. I wrote a normalization function that:
  - Lowercases the text
  - Strips punctuation and extra spaces
  - Handles missing values gracefully

- **How I approached grouping:**
  - **Normalization:** Cleaned names to make them easier to compare.
  - **Blocking:** To save compute time, I grouped records by the first character of their normalized name—so I only compare records likely to be related.
  - **Fuzzy matching:** I used a similarity threshold (90) with a token-based comparator so “Acme Inc” and “Acme Incorporated” can still match.
  - **Graph clustering:** If A is similar to B, and B is similar to C, I treat A–B–C as one group. This helps catch near-matches that wouldn’t be caught with just one-to-one comparisons.
