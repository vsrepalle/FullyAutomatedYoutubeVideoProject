import os
import json
from moviepy.editor import *
from moviepy.video.fx.all import speedx, crop

# Global Settings for 9:16 Shorts
W, H = 1080, 1920
FPS = 24

def ensure_rgb(clip):
    """FORCES 1-channel masks into 3-channel RGB to prevent broadcasting errors."""
    return clip.on_color(size=(W, H), color=(0,0,0), col_opacity=0).set_opacity(1)

def get_full_screen_image(img_path, duration):
    """Resizes and crops images to fill 1080x1920 perfectly (No Black Bars)."""
    if not os.path.exists(img_path):
        # Fallback to a solid color if image is missing
        return ColorClip(size=(W, H), color=(20, 20, 20), duration=duration)
    
    clip = ImageClip(img_path).set_duration(duration)
    
    # Calculate scale to cover the entire 1080x1920 area
    scale_factor = max(W / clip.w, H / clip.h)
    
    # Resize then crop from center
    clip = clip.resize(scale_factor)
    clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=W, height=H)
    
    return clip

def create_video_from_json(json_path, output_name):
    with open(json_path, 'r') as f:
        data = json.load(f)

    final_clips = []
    
    for i, item in enumerate(data):
        # 1. Base Image Layer (Zoomed & Cropped)
        img_path = f"assets/images/scene_{i}.jpg" # Ensure your downloader saves here
        duration = 8.0 # Standard for Shorts
        base_layer = get_full_screen_image(img_path, duration)
        
        # 2. Headline Clip (with ensure_rgb fix)
        headline = TextClip(
            item['headline'].upper(),
            fontsize=70, color='yellow', font='Arial-Bold',
            method='caption', size=(W-100, None)
        ).set_duration(duration).set_position(('center', 100))
        headline = ensure_rgb(headline)

        # 3. Hook Text Clip
        hook = TextClip(
            item['hook_text'],
            fontsize=50, color='white', font='Arial',
            method='caption', size=(W-150, None)
        ).set_duration(duration).set_position(('center', 400))
        hook = ensure_rgb(hook)

        # 4. Details Text (The core news/fact)
        details = TextClip(
            item['details'],
            fontsize=45, color='white', font='Arial',
            method='caption', size=(W-120, None),
            bg_color='black'
        ).set_duration(duration).set_position(('center', 'center'))
        details = ensure_rgb(details)

        # 5. Subscribe Hook (Logic for ExamPulse and WonderFacts)
        sub_hook_text = item.get('subscribe_hook', "NONE")
        if sub_hook_text != "NONE":
            sub_clip = TextClip(
                sub_hook_text,
                fontsize=40, color='cyan', font='Arial-Bold',
                method='caption', size=(W-100, None)
            ).set_duration(duration).set_position(('center', H-300))
            sub_clip = ensure_rgb(sub_clip)
            scene = CompositeVideoClip([base_layer, headline, hook, details, sub_clip])
        else:
            scene = CompositeVideoClip([base_layer, headline, hook, details])

        final_clips.append(scene)

    # Concatenate and apply 1.2x speed for punchy engagement
    final_video = concatenate_videoclips(final_clips, method="compose")
    final_video = speedx(final_video, factor=1.2)

    # Export
    output_path = f"output/{output_name}.mp4"
    final_video.write_videofile(output_path, fps=FPS, codec="libx264", audio_codec="aac")
    print(f"✅ Video rendered at: {output_path}")

if __name__ == "__main__":
    # Test run with your latest WonderFacts JSON
    create_video_from_json('../json/current_batch.json', 'WonderFacts_Ep1')