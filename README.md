## Information Retrieval System (IRS) for Video Games

**Authors:**

- José Miguel Zayas Pérez - C-312
- Adrian Hernandez Santos - C-311

**Course:** Computer Science, MATCOM, UH

**Project Link:** [https://github.com/josem-nex/irs-project/](https://github.com/josem-nex/irs-project/)

**Full Report:** [https://github.com/josem-nex/irs-project/Report.pdf](https://github.com/josem-nex/irs-project/Report.pdf)

This project implements a simple search engine for video games based on a dataset of approximately 25,000 games scraped from the gg.deals website. The system aims to return relevant video games based on user queries by utilizing three different similarity strategies:

- **Vectorial Model:** This approach uses TF-IDF to convert game descriptions and user queries into feature vectors, comparing them using cosine similarity.
- **Tag-Based Similarity:** This method calculates similarity based on the number of shared tags between the query and game.
- **Genre-Based Similarity:** This approach calculates similarity based on the number of shared genres between the query and game.

The final similarity score is calculated by averaging the normalized similarity values from each strategy, providing a score between 0 and 1 for each game.

### Implementation details:

- **Languages & Libraries:** Python, Scrapy, Gensim, Spacy, SQLAlchemy, FastAPI
- **Data Acquisition:** Scraped from gg.deals using Scrapy.
- **Data Preprocessing:** Tokenization, stop word removal, and lemmatization using Spacy.
- **User Interface:** Simple web page using FastAPI.
- **Result Transparency:** Individual similarity values for each strategy are displayed to the user, allowing them to understand the reasons behind the recommendations.

### Potential Improvements:

- **Semantic Checking:** The current system lacks semantic understanding of user queries, potentially leading to irrelevant results.
- **Boolean Model:** Implementing a Boolean model based on tags and genres could improve the search space, but requires a robust query processing mechanism.
- **Recommendation System:** A recommendation system based on user search history could be implemented to provide personalized recommendations.
