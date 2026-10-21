
from transformers import pipeline

model_name = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

chatbot = pipeline(
    "text-generation",
    model=model_name,
)

mode = input("Choose mode (angry/funny/sad): ").lower()

system_prompt = {
    "angry": "Respond in an exaggerated angry tone.",
    "funny": "Be a funny chatbot and use jokes.",
    "sad": "Respond in a sad and emotional tone."
}.get(mode, "You are a friendly chatbot.")

messages = [
    {"role": "system", "content": system_prompt}
]

print("Chatbot ready! Type 0 to exit.")

while True:
    prompt = input("You: ")

    if prompt == "0":
        break

    messages.append({"role": "user", "content": prompt})

    result = chatbot(
        messages,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.8,
    )

    reply = result[0]["generated_text"][-1]["content"]
    print("Bot:", reply)

    messages.append({"role": "assistant", "content": reply})
