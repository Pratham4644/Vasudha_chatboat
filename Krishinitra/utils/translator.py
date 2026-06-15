from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def translate_text(text, source_lang, target_lang):

    tokenizer.src_lang = source_lang

    inputs = tokenizer(text, return_tensors="pt")

    target_token_id = tokenizer.convert_tokens_to_ids(target_lang)

    generated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=target_token_id,
        max_length=400
    )

    translated_text = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True
    )[0]

    return translated_text