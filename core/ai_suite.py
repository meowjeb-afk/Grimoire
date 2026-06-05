import os
import cv2
import torch
import numpy as np
from PIL import Image, ImageOps

# Safe import wrapper for heavy dependencies
HEAVY_DEPS_AVAILABLE = False
try:
    from rembg import remove
    from diffusers import StableDiffusionInpaintPipeline, StableDiffusionXLImg2ImgPipeline
    HEAVY_DEPS_AVAILABLE = True
except ImportError:
    print("Warning: Heavy AI dependencies missing. Run: pip install opencv-python torch diffusers rembg")

if HEAVY_DEPS_AVAILABLE:
    class DesignSuite:
        def __init__(self, hf_auth_token=None):
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.token = hf_auth_token
            print(f"DesignSuite initialized running on: {self.device.upper()}")

        def subject_isolator(self, input_image_path, output_image_path):
            print("[Processing] Isolating subject and removing background...")
            with open(input_image_path, 'rb') as i:
                input_data = i.read()
            output_data = remove(input_data)
            with open(output_image_path, 'wb') as o:
                o.write(output_data)
            print(f"[Success] Isolated image saved to {output_image_path}")
            return output_image_path

        def context_aware_inpaint(self, image_path, mask_path, prompt, output_path):
            print("[Processing] Initializing Neural Inpainting Pipeline...")
            pipe = StableDiffusionInpaintPipeline.from_pretrained(
                "runwayml/stable-diffusion-inpainting",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            # VRAM Optimization for 8GB cards
            pipe.enable_attention_slicing() 
            init_image = Image.open(image_path).convert("RGB").resize((512, 512))
            mask_image = Image.open(mask_path).convert("RGB").resize((512, 512))
            image = pipe(prompt=prompt, image=init_image, mask_image=mask_image).images[0]
            image.save(output_path)
            print(f"[Success] Inpainted asset saved to {output_path}")
            return output_path

        def super_resolution_upscaler(self, image_path, output_path, scale_factor=4):
            print(f"[Processing] Upscaling image by {scale_factor}x...")
            img = cv2.imread(image_path)            if img is None: raise Exception("Failed to load image for upscaling.")
            width = int(img.shape[1] * scale_factor)
            height = int(img.shape[0] * scale_factor)
            dim = (width, height)
            upscaled = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(output_path, upscaled)
            print(f"[Success] High-res asset saved to {output_path}")
            return output_path

        def palette_harmonizer(self, image_path, num_colors=5):
            print("[Processing] Analyzing color frequencies...")
            img = Image.open(image_path).convert('RGB').resize((50, 50))
            colors = img.getcolors(2500)
            sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)
            dominant_colors = sorted_colors[:num_colors]
            hex_palette = ['#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2]) for count, rgb in dominant_colors]
            print(f"[Success] Extracted Palette: {hex_palette}")
            return ", ".join(hex_palette)

        def style_transfer_refiner(self, base_image_path, style_prompt, output_path):
            print(f"[Processing] Remapping visual DNA to style: '{style_prompt}'...")
            pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-refiner-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            # VRAM Optimization for 8GB cards
            pipe.enable_attention_slicing()
            init_image = Image.open(base_image_path).convert("RGB").resize((768, 768))
            image = pipe(prompt=style_prompt, image=init_image, strength=0.3).images[0]
            image.save(output_path)
            print(f"[Success] Styled asset saved to {output_path}")
            return output_path

        def seamless_texture_tiler(self, image_path, output_path):
            print("[Processing] Transforming asset into tileable pattern...")
            img = Image.open(image_path)
            w, h = img.size
            flipped_h = ImageOps.mirror(img)
            flipped_v = ImageOps.flip(img)
            flipped_both = ImageOps.flip(flipped_h)
            seamless = Image.new('RGB', (w * 2, h * 2))
            seamless.paste(img, (0, 0))
            seamless.paste(flipped_h, (w, 0))
            seamless.paste(flipped_v, (0, h))
            seamless.paste(flipped_both, (w, h))
            seamless.save(output_path)
            print(f"[Success] Tileable pattern saved to {output_path}")
            return output_path

    class AdvancedDesignExtensions:        def __init__(self, device="cuda"):
            self.device = device if torch.cuda.is_available() else "cpu"
            print(f"AdvancedDesignExtensions initialized on: {self.device.upper()}")

        def generate_pbr_maps(self, diffuse_image_path, prefix_output_path):
            print("[Processing] Generating physical PBR surface coordinates...")
            gray = cv2.imread(diffuse_image_path, cv2.IMREAD_GRAYSCALE)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            normal_map = np.zeros((gray.shape[0], gray.shape[1], 3), dtype=np.uint8)
            dx = sobelx * 2.0
            dy = sobely * 2.0
            dz = np.ones_like(gray) * 255.0
            norm = np.sqrt(dx**2 + dy**2 + dz**2)
            normal_map[..., 0] = ((dx / norm) * 127.5 + 127.5).astype(np.uint8)
            normal_map[..., 1] = ((dy / norm) * 127.5 + 127.5).astype(np.uint8)
            normal_map[..., 2] = ((dz / norm) * 255.0).astype(np.uint8)
            cv2.imwrite(f"{prefix_output_path}_normal.png", normal_map)
            cv2.imwrite(f"{prefix_output_path}_displacement.png", gray)
            print(f"[Success] Exported print-ready PBR maps to: {prefix_output_path}_normal.png")
            return f"{prefix_output_path}_normal.png"

        def composite_layers(self, foreground_png, background_jpg, position=(0,0)):
            print("[Processing] Intersecting alpha mask transparency layers...")
            bg = Image.open(background_jpg).convert("RGBA")
            fg = Image.open(foreground_png).convert("RGBA")
            bg.paste(fg, position, fg)
            final_rgb = bg.convert("RGB")
            output_path = os.path.join(os.path.dirname(foreground_png), "final_studio_composite.jpg")
            final_rgb.save(output_path)
            print(f"[Success] Composited artwork layer layout flattened to: {output_path}")
            return output_path