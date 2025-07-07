
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Default instruction (can be overridden via Streamlit input)
template = (
    "Give me all the reviews and ratings of this product which are given by customers on the product. "
    "Here is the DOM content:\n{dom_content}\n\nInstruction:\n{parse_description}"
)

model = OllamaLLM(model="moondream")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({
            "dom_content": chunk,
            "parse_description": parse_description
        })
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(str(response))

    return "\n\n".join(parsed_results)
