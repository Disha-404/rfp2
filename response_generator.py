import openai
from config import API_KEY, BASE_URL, MODEL_NAME

def generate_response(requirement, similar_texts, similar_responses, similar_comments, similar_product):
    product_description = similar_product
    prompt = f"The following requirement was given for the product ({product_description}): {requirement}\n\n"
    for i, (text, response, comment, product) in enumerate(zip(similar_texts, similar_responses, similar_comments, similar_product)):
        prompt += f"Similar requirement {i+1}: {text}\nResponse: {response}\nComment: {comment}\nproduct{product}\n\n"
    prompt += ("With no prior understanding if the functionality is possible with the similar texts, their responses, and comments,"
               "generate the response 'Yes' when the similar texts and their responses suggest that the given requirement can surely be fulfilled without a doubt,"
               "'No' when it suggests the requirement is not related to the similar texts,"
               "'Customizable' when the functionality exists but for a different requirement but can be done,"
               "'Partially Supported' when it can partially fulfill and a comment on how much of the requirement is done and how,"
               "or 'Not sure' when the information given is not sufficient to predict based on the similar requirement and comments with no comment or when there is no text to refer."
               "Final generation should be of kind Response \n Comment. "
               "Comment is short statement describing functionality it is providing and how."
               "Please dont mention the words: similar requirement in the comment.Make the comment look like the {similar_comments} or a functionality statement")

    client = openai.OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )

    chat_completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a great consultant for a Fin Tech company and not a chatbot. Provide a response to the requirement and a comment stating the product functionality based off the context so that the user understands more about the offering. comment is not the reasoning behind your response. Response is based of your undertsanding , if the requirement can be offered or not, a Yes, No, Customisable, Partially Supported, Not sure.Dont mention the similar texts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=128
    )

    response = chat_completion.choices[0].message.content
    return response
