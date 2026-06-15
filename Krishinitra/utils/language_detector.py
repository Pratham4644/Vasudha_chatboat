try:
    from .translator import translate_text
except (ImportError, SystemError):
    # When running this module as a script, the package context may not be set
    from translator import translate_text

text = "ऊस लागवड कशी करावी?"

result = translate_text(
    text,
    "mar_Deva",
    "eng_Latn"
)

print(result)