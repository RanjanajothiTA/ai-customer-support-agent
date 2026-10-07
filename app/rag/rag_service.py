from google import genai
from dotenv import load_dotenv
from rag.retriever import search
from google.genai.errors import ServerError, ClientError

load_dotenv()

client=genai.Client()

def retrieve_context(query, top_k=3):
    results = search(query, top_k)

    return results
def build_context(results):
    context = ""

    for result in results:
        context += result["chunk"]["text"] + "\n\n"

    return context

def generate_rag_response(query):
    results = retrieve_context(query)

    context = build_context(results)

    prompt = f"""
You are a ShopEase customer support assistant.

Use the following ShopEase knowledge base context to answer the customer's question.

Knowledge base context:
{context}

Customer question:
{query}

Answer the question using only the information provided in the knowledge base context.
If the answer cannot be found in the context, say that you do not have enough information to answer.
Do not invent or assume information.
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return {
            "answer": response.text,
            "sources": [
            {
                "source": result["chunk"]["source"],
                "chunk_id": result["chunk"]["chunk_id"]
            }
            for result in results
        ]
    }
    except ServerError:
        return {
            "answer": "I'm sorry, the AI service is temporarily unavailable. Please try again in a moment.",
            "sources": []
        }

    except ClientError:
        return {
            "answer": "I'm sorry, there was a problem with the AI request. Please try again later.",
            "sources": []
        }

    except Exception:
        return {
            "answer": "I'm sorry, something went wrong while generating the response.",
            "sources": []
        }


if __name__ == "__main__":
    query = "How many days do I have to return a product?"

    answer = generate_rag_response(query)

    print("Question:")
    print(query)

    print("\nRAG Answer:")
    print(answer)