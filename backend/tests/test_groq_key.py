from app.ai.llm import llm_service

def test_groq():
    prompt = "Extract product from: Amoxicillin 250mg Capsules Batch #AMX-998"
    sys_p = 'Return JSON in exact format: {"product_name": "string"}'
    result = llm_service.invoke(prompt=prompt, system_prompt=sys_p, response_format_json=True)
    print("=" * 60)
    print("LIVE GROQ API INFERENCE RESPONSE:")
    print(result.encode('ascii', 'ignore').decode('ascii'))
    print("=" * 60)

if __name__ == "__main__":
    test_groq()
