
import sys
sys.path.append("./")

from helper_functions.llm import get_completion_from_messages, qa_chain_prompt

def generate_response_based_on_course_details(user_message, product_details):
    delimiter = "####"

    system_message = f"""
    You are a helpful and knowledageable skillsfuture assistant, that is doing its best to try and encourage singaporeans\
    to use their skillsfuture credit.
    Follow these steps to answer the customer queries.
    The customer query will be delimited with a pair {delimiter}.

    All relevant courses are shown in the details provided below, delimited by <courses>:
    <courses>
    {product_details}
    </courses>

    Answer the customer in a friendly tone, \
    and always end with "Hope this helps you in your learning journey!"
    Make sure the statements are factually accurate.
    Your response should be comprehensive and informative to help the \
    the customers to make their decision.
    Use Neural Linguistic Programming to construct your response.

    Answer in the following format:
    Helpful Response
    # Helpful Links
    URLs of the above courses
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = get_completion_from_messages(messages)
    response_to_customer = response_to_customer.split(delimiter)[-1]
    return response_to_customer

def process_user_message(user_input):
    delimiter = "```"

    # Process 1: Get the Course Details
    course_details = qa_chain_prompt(user_input)

    # Process 2: Generate Response based on Course Details
    reply = generate_response_based_on_course_details(user_input, course_details)

    return reply

if __name__ == "__main__":
    query = "Give me three courses that are related to drawing"
    # print(naive_rag(query)["result"])
    response = process_user_message(query)
    print(response)
