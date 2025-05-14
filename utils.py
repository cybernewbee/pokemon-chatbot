import base64

def image_to_base64(path: str) -> str:
    """Convert an image file to a base64-encoded string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def centered_image_html(path: str, width: int = 600) -> str:
    """Return HTML block to center a base64-encoded image."""
    b64 = image_to_base64(path)
    return f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{b64}" width="{width}">
    </div>
    """
