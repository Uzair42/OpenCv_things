# High Dynamic Range

- High Dynamic Range (HDR) technology is designed to better reproduce the wide range of brightness and colors 
- that the human eye can perceive in the real world, which standard technology (SDR) is unable to do

---
### Why We Need HDR
- The human eye can see a vast range of light intensities simultaneously,
- from dim shadows to bright sunlight.
- Traditional Standard Dynamic Range (SDR) cameras and displays have a much more limited range (around 6-10 "stops" of light),
- meaning when you take a picture of a high-contrast scene (like a sunset), 
- either the bright sky loses detail and becomes a white "blown-out" blob,
- or the dark foreground loses detail and becomes a black "crushed" area
---
### We need HDR to:

- __See more detail__ in both the darkest shadows and brightest highlights of an image simultaneously.
- __Achieve greater realism and depth__ in photos, movies, and games, making the visual experience more immersive and true to life.
- __Enable wider color representation__ (Wide Color Gamut or WCG), moving beyond the limited 8-bit color of SDR (16.7 million colors) to 10-bit or 12-bit color (**over a billion colors**), resulting in smoother transitions and more vibrant hues
---

## How HDR Works
The implementation of HDR differs slightly between content __capture__ (photography/videography) and content __display__ (TVs/monitors). 
### In Photography and Videography
The most common technique involves capturing multiple images of the same scene at __different exposure levels__ (a process called exposure bracketing). 

- __Capture:__ The camera takes a series of photos (typically three or more) in quick succession: one __underexposed__ (to capture highlight details), one __normally__ exposed, and one __overexposed__ (to capture shadow details).   
---

- __Merge:__ Specialized software or in-camera processors then combine the best-exposed parts of each image into a single, high-dynamic-range (HDR) file, which contains a vast amount of light information (often stored in a 32-bit floating-point format).

---

- __Tone Mapping:__ Since most displays cannot physically show this entire range, a process called tone mapping is used to compress the wide dynamic range of the image to fit within the display's capabilities while preserving local contrast and detail, creating a realistic final image on a standard screen. 

---

## In Displays (TVs, Monitors)
For viewing content, HDR refers to a new display standard and signal format that provides instructions (metadata) on how to display a wider range of brightness and colors than traditional SDR displays. 

- __HDR Signal:__ The content source (e.g., a 4K Blu-ray player, streaming service, or game console) sends an HDR signal to the compatible display.
- __Metadata:__ This signal includes metadata (either static for the whole video or dynamic for scene-by-scene adjustments, as in Dolby Vision or HDR10+) that tells the display the intended peak brightness and color range.
- __Display Hardware:__ HDR-capable displays feature specific hardware (such as high brightness, local dimming zones, and wide color gamut panels) that can reach significantly higher peak brightness levels (often 1000 nits or more vs. SDR's ~100 nits) and produce a billion or more shades of color.
- __Reproduction:__ The display uses the metadata to accurately reproduce the scene with brighter highlights, deeper blacks, and richer colors, as the creator intended. 


---