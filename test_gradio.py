# Save as test_gradio.py
import gradio as gr

def greet(name): return f"Hello, {name}!"

gr.Interface(fn=greet, inputs="text", outputs="text").launch(share=False, inbrowser=True)
