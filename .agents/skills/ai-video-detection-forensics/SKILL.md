---
name: ai-video-detection-forensics
description: >-
  The 200-principle master reference for AI video detection and forensic media analysis.
  Covers Google SynthID detection, C2PA Content Credentials, metadata analysis, temporal
  consistency, anatomical and physics heuristics, multimodal audio-visual alignment, and
  verification workflows using FFmpeg, MediaInfo, and frame extraction.
metadata:
  version: 1.0.0
license: MIT
---

# AI-Generated Video Detection & Forensics (2026 Reference)

Technical reference and methodology for verifying whether video media was generated or altered by AI models (specifically Google Flow and Veo), inspecting cryptographic provenance, and conducting digital forensics.

---

## 1. Primary Verification Methods

| Method | Evidence Strength | Description |
|---|---|---|
| **Google SynthID Detector** | Strong | Deep-learning embedded digital watermark check across video and audio streams. Identifies Google AI origin. |
| **Gemini Verification** | Strong | Analyzes media up to 100MB / 90s for Google AI audio/visual generation markers and segment timestamps. |
| **C2PA Content Credentials** | Strong for recorded claims | Cryptographically signed metadata tracking generation models, edits, and tool history. |
| **Container & Stream Metadata** | Supporting | Analysis of encoder tags, atom hierarchies, and audio/video stream multiplexing signatures. |
| **Visual & Physical Heuristics** | Heuristic clue | Analysis of temporal flicker, anatomical consistency, lighting vectors, and motion physics. |

---

## 2. Master Catalog: 200 AI-Video Detection Principles

### A. Watermarks, Provenance, and Original-File Verification (1–20)
1. **SynthID Video Detection**: Scan video stream latents for Google's embedded neural watermark.
2. **SynthID Audio Detection**: Independently inspect audio spectrum for embedded generation watermarks.
3. **Segment-Level Verification**: Isolate exact start and end timestamps where synthetic signals test positive.
4. **Visual Watermark Inspection**: Audit corner badges and on-screen generation text indicators.
5. **Watermark Authenticity**: Differentiate authentic machine verification from easily duplicated or removed visual logos.
6. **C2PA Manifest Detection**: Scan file containers for signed Content Credentials headers.
7. **Cryptographic Signature Validation**: Confirm that embedded public-key signatures have not been broken or invalidated.
8. **Certificate Trust Validation**: Trace the signing certificate authority to a recognized credential trust list.
9. **Generation Action History**: Verify whether manifest actions record an initial synthetic generation event.
10. **Editing Action History**: Review documented post-generation edits, crops, and color corrections.
11. **Source Ingredient Inspection**: Review hash links to base reference images or source clips.
12. **Claimed Generator Identification**: Read embedded metadata declaring model variant or software engine.
13. **Original File Acquisition**: Analyze unmodified camera or server downloads rather than recompressed social uploads.
14. **Source-File Checksum**: Compute and record SHA-256 hashes to establish forensic custody.
15. **Project Provenance**: Cross-reference asset IDs against Google Flow studio project databases.
16. **Creator Disclosure**: Audit creator text declarations against platform mandatory disclosure rules.
17. **Verified Upload History**: Locate the earliest public posting date and initial publisher profile.
18. **Signed Camera-Origin Evidence**: Verify hardware-level sensor attestations (e.g. Sony, Leica, Canon C2PA).
19. **Watermark Persistence Testing**: Compare detector sensitivity across original and re-encoded revisions.
20. **Negative-Evidence Restraint**: Treat absence of detectable watermarks as inconclusive, never as proof of real camera capture.

### B. File Metadata and Encoding Analysis (21–35)
21. **Container Inspection**: Parse MP4, MOV, and MKV atom structures (`moov`, `trak`, `udta`).
22. **Video Codec Inspection**: Verify whether profile, level, and pixel format match typical generator defaults.
23. **Encoder Metadata Inspection**: Inspect software identification tags (e.g. `encoder: Google`).
24. **Creation-Time Analysis**: Compare container creation timestamps with claimed real-world event chronology.
25. **Frame-Rate Verification**: Verify exact fractional frame rate (e.g. 24.000 vs 23.976 fps).
26. **Variable-Frame-Rate Analysis**: Detect irregular frame duration timestamps indicating software synthesis.
27. **Resolution History**: Inspect scaling artifacts indicating non-native upsampling.
28. **Color Metadata Validation**: Verify NCLC tags, transfer characteristics, and matrix coefficients.
29. **Audio-Track Inspection**: Identify synthetic dual-mono, missing channels, or abnormal sample rates.
30. **Video-Audio Duration Comparison**: Detect millisecond discrepancies between audio and video stream lengths.
31. **File Remuxing Indicators**: Identify signs of repackaging or container rebuilding.
32. **Re-Encoding History**: Trace multiple generations of lossy compression artifacts.
33. **GOP and Keyframe Analysis**: Check keyframe distance, B-frame structure, and slice headers.
34. **Compression Discontinuity Analysis**: Detect sudden shifts in macroblock quantization parameters.
35. **Metadata-Absence Interpretation**: Recognize that stripped metadata occurs routinely in authentic web exports.

### C. Temporal Consistency and Frame-to-Frame Artifacts (36–55)
36. **Identity Persistence**: Verify whether human facial identity remains identical across entire takes.
37. **Facial Texture Persistence**: Monitor skin pore structure for unnatural frame-to-frame shifting.
38. **Object Shape Persistence**: Audit inanimate objects for subtle geometric morphing.
39. **Texture Flickering**: Detect high-frequency noise or textural boiling on detailed surfaces.
40. **Background Stability**: Confirm stationary background architectures maintain rigid physical boundaries.
41. **Edge Stability**: Audit high-contrast edges for swimming pixels or phase chatter.
42. **Motion Continuity**: Track whether moving objects follow unbroken kinematic trajectories.
43. **Object Permanence**: Check whether small background items vanish or appear without physical cause.
44. **Occlusion Recovery**: Verify that occluded elements reappear with accurate geometry and coloring.
45. **Temporal Color Stability**: Inspect overall scene color balance for unexplained second-to-second drift.
46. **Temporal Illumination Stability**: Detect illumination changes lacking on-screen light source triggers.
47. **Character Continuity**: Track buttons, jewelry, collars, and accessory placements.
48. **Scene Geometry Consistency**: Ensure room boundaries and spatial ratios remain mathematically rigid.
49. **Frame Duplication Analysis**: Detect repeated frame pairs inserted to pad duration.
50. **Frame Interpolation Anomalies**: Identify optical flow tearing on fast-moving edges.
51. **Optical-Flow Consistency**: Map dense optical flow vectors to detect direction contradictions.
52. **Motion-Boundary Stability**: Inspect boundaries between moving foreground subjects and static backdrops.
53. **Foreground-Background Alignment**: Check parallax rates between camera motion and depth planes.
54. **Motion Blur Consistency**: Verify whether shutter blur length matches physical travel speed.
55. **Long-Range Temporal Coherence**: Track whether narrative elements remain physically stable over 8+ seconds.

### D. Faces, Eyes, Expressions, and Speech (56–75)
56. **Facial Symmetry Anomalies**: Check for unnatural bilateral face deformation.
57. **Eye Geometry Consistency**: Inspect iris roundness and sclera shape through eye travel.
58. **Pupil Position Consistency**: Verify that gaze axes converge plausibly on target objects.
59. **Eye Reflection Consistency**: Compare specular catchlights across both eyes against scene lights.
60. **Natural Blinking**: Audit blink frequency, duration, and complete eyelid closure mechanics.
61. **Eyelash and Eyebrow Stability**: Track micro-features for swimming or blurring during movement.
62. **Teeth Continuity**: Count and inspect visible dental structures for shifting numbers or alignment.
63. **Tongue Movement Plausibility**: Check tongue articulation during phoneme delivery.
64. **Lip Synchronization**: Confirm visible lip closures (`/p/`, `/b/`, `/m/`) match audio transients.
65. **Mouth Interior Consistency**: Audit oral cavity depth, shadows, and roof anatomy during speech.
66. **Jaw Articulation**: Verify vertical and lateral mandibular movement matches vocal mechanics.
67. **Facial Muscle Coordination**: Check whether brow and cheek muscle groups contract in emotional harmony.
68. **Expression-Transition Continuity**: Audit emotional transitions for sudden unnatural shifts.
69. **Head-Pose Geometry**: Track perspective scaling of nose and ears through three-dimensional head turns.
70. **Ear Continuity**: Verify earlobe attachment, cartilage folds, and symmetry against the skull.
71. **Hairline Continuity**: Audit hair growth boundaries and individual strand grouping during movement.
72. **Skin-Detail Continuity**: Track moles, freckles, and wrinkles across varying angles.
73. **Facial Occlusion Consistency**: Inspect facial boundaries when hands or glasses pass in front.
74. **Face-Neck Alignment**: Check anatomical continuity between jawline, neck tendons, and clavicle.
75. **Speech-Emotion Alignment**: Verify that vocal intensity corresponds to facial expression energy.

### E. Hands, Bodies, Anatomy, and Clothing (76–95)
76. **Finger-Count Consistency**: Verify presence of exactly five digits per hand on all visible grips.
77. **Finger-Joint Plausibility**: Audit interphalangeal joints for impossible reverse bending.
78. **Finger-Length Stability**: Track digit proportions through grasping motions.
79. **Hand-Object Contact**: Confirm fingers wrap around objects with authentic physical collision.
80. **Grip Mechanics**: Ensure thumb opposes fingers correctly when holding tools or cups.
81. **Palm Orientation**: Check anatomical alignment between wrist rotation and palm direction.
82. **Wrist Articulation**: Inspect carpals for unnatural twisting or thinning.
83. **Arm-Length Consistency**: Measure limb proportions throughout reaching motions.
84. **Shoulder-Elbow Coordination**: Verify natural kinematic chain movement across joints.
85. **Foot-Floor Contact**: Confirm shoe soles rest flat on the ground plane without floating or clipping.
86. **Walking-Gait Continuity**: Track heel-strike and toe-off phases across repeated strides.
87. **Running Mechanics**: Check flight phase and torso lean for gravitational realism.
88. **Body Balance**: Verify center of mass remains supported by the stance base.
89. **Weight-Transfer Realism**: Audit hip and shoulder shifts when changing direction.
90. **Garment Topology**: Track fabric seams, zippers, and pocket alignments across movement.
91. **Clothing-Logo Consistency**: Verify brand lettering and graphics do not shift or scramble.
92. **Fabric-Fold Continuity**: Inspect cloth folds for physical persistence during motion.
93. **Accessory Persistence**: Confirm watches, belts, and glasses remain attached to identical locations.
94. **Hair Dynamics**: Compare hair sway with head acceleration and environmental wind.
95. **Skin-Clothing Boundaries**: Audit intersections between cloth edges and skin for rendering clipping.

### F. Objects, Backgrounds, Textures, and Text (96–115)
96. **Text Legibility**: Inspect signs and screens for garbled or pseudo-linguistic characters.
97. **Text Persistence**: Verify that words remain identical across successive frames.
98. **Logo Consistency**: Confirm commercial trademarks maintain accurate proportions.
99. **Signage Stability**: Audit street signs and posters for drifting letters during camera motion.
100. **Repeated Texture Anomalies**: Identify cloned texture tiles in backgrounds or foliage.
101. **Architectural Geometry**: Check doorframes, brickwork, and beams for straightness and right angles.
102. **Perspective Convergence**: Verify that parallel environmental lines converge to coherent vanishing points.
103. **Object-Count Persistence**: Track background props to ensure items do not multiply or vanish.
104. **Object-Size Consistency**: Verify that object dimensions scale strictly with perspective distance.
105. **Surface Reflection Consistency**: Audit metallic and glossy surfaces for accurate environment reflections.
106. **Transparent-Material Rendering**: Inspect glass refraction and transmission for physical plausibility.
107. **Mirror Reflection Matching**: Confirm mirror images match the angle and posture of subjects.
108. **Background-Person Continuity**: Audit secondary human figures for warping or missing limbs.
109. **Background-Object Interaction**: Confirm background actors interact believably with furniture.
110. **Fine-Pattern Stability**: Check fences, grates, and micro-patterns for moiré or swimming lines.
111. **Vehicle Geometry**: Inspect wheel roundness, chassis symmetry, and tire tread contact.
112. **License-Plate Consistency**: Confirm license plate alphanumeric strings remain stable.
113. **Product-Shape Consistency**: Audit commercial product containers for geometric deformation.
114. **Reappearing-Object Continuity**: Check objects that leave the frame and return for altered features.
115. **Scene-Detail Coherence**: Confirm background technology and props match the stated setting.

### G. Physics and Real-World Behavior (116–135)
116. **Gravity Consistency**: Verify falling objects accelerate at 9.8 m/s² equivalent trajectory.
117. **Inertia Consistency**: Confirm moving bodies require force to decelerate or pivot.
118. **Momentum Conservation**: Audit collisions for reciprocal energy transfer between objects.
119. **Collision Mechanics**: Confirm solid bodies do not pass through each other.
120. **Object Deformation**: Ensure rigid items do not bend like rubber upon light contact.
121. **Liquid Flow Consistency**: Audit liquid streams for droplet separation, surface tension, and viscosity.
122. **Fluid-Container Interaction**: Confirm poured fluids fill volume without phantom leakage.
123. **Particle Trajectories**: Check dust, rain, and spark paths against wind and gravity vectors.
124. **Smoke Movement**: Inspect smoke plumes for turbulent diffusion and thermal expansion.
125. **Fire Behavior**: Verify flame flicker rate, updraft direction, and combustion source attachment.
126. **Wind Response**: Confirm trees, flags, and hair bend in matching directions from wind.
127. **Water Reflection Behavior**: Audit water wavelets for accurate dynamic reflection displacement.
128. **Water-Surface Interaction**: Check boat hulls and swimmers for plausible wakes and bow waves.
129. **Contact-Shadow Behavior**: Verify presence of ambient occlusion shadows where objects touch ground.
130. **Rolling Mechanics**: Check that rolling wheels rotate at a rate matching linear ground velocity.
131. **Vehicle Motion**: Confirm vehicles lean outward slightly during aggressive turns.
132. **Trajectory Smoothness**: Identify impossible abrupt velocity changes in projectile paths.
133. **Mechanical Interaction**: Confirm gears mesh, levers pivot at fulcrums, and latches catch.
134. **Biological Motion**: Verify animal quadrupeds adhere to biological footfall sequences.
135. **Physical Causality**: Confirm every physical effect is preceded by an observable cause.

### H. Lighting, Optics, and Camera Behavior (136–150)
136. **Light-Source Consistency**: Verify that highlights on all subjects originate from the same vector.
137. **Shadow-Direction Consistency**: Confirm cast shadows project away from visible light sources.
138. **Shadow Softness Consistency**: Check that shadow edge blur matches source distance and aperture.
139. **Reflection-Light Correspondence**: Confirm bright light sources appear in specular highlights.
140. **Depth-of-Field Behavior**: Verify that blur circles increase smoothly with focal distance.
141. **Lens-Distortion Consistency**: Check that barrel or pincushion distortion curves symmetrically.
142. **Camera Parallax**: Confirm foreground objects shift faster across the frame than distant backdrops.
143. **Camera Trajectory Coherence**: Verify camera movements follow physically mountable paths.
144. **Camera-Object Geometry**: Check perspective distortion against stated lens focal length.
145. **Exposure Continuity**: Verify lighting level shifts have identifiable on-screen causes.
146. **Highlight Behavior**: Audit blown highlights for organic roll-off rather than gray flat spots.
147. **Motion-Blur Direction**: Confirm directional blur aligns with combined camera/subject vectors.
148. **Focus-Tracking Plausibility**: Check that focus pulls follow human reaction timing.
149. **Image-Noise Consistency**: Verify sensor noise grain matches across shadow, midtone, and highlight.
150. **Lens-Artifact Consistency**: Confirm chromatic aberration and flaring emanate from light sources.

### I. Generated Speech, Sound, and Audio-Visual Coherence (151–170)
151. **Speech-Lip Alignment**: Match phonetic plosives, fricatives, and vowels to lip shape.
152. **Voice Identity Continuity**: Detect sudden spectral timbre changes across a single speaker.
153. **Prosody Plausibility**: Audit vocal cadence, sentence stress, and interrogative inflection.
154. **Emotional Voice Consistency**: Check whether vocal tone matches visible facial anguish or joy.
155. **Breathing Continuity**: Listen for inhalation pauses preceding long vocal lines.
156. **Vocal Micro-Artifacts**: Detect robotic vocoder phase buzz or metallic resonance in dialogue.
157. **Consonant Clarity Consistency**: Audit high-frequency consonants for sudden dulling or mushiness.
158. **Vowel Transition Smoothness**: Listen for digital stepping between formant frequencies.
159. **Speech Rhythm Naturalness**: Detect machine pacing lacking natural micro-hesitations.
160. **Room Acoustics Consistency**: Verify reverb character matches visible room dimensions and surfaces.
161. **Reverb-Environment Matching**: Confirm vocal reflections match concrete, wood, or open-air settings.
162. **Footstep Synchronization**: Lock shoe impact audio to visible ground contact frames.
163. **Object-Impact Synchronization**: Lock collision audio transients to contact frames.
164. **Ambient Continuity**: Detect sudden cuts or dropouts in room tone beds.
165. **Sound-Source Localization**: Check stereo panning matches on-screen horizontal positioning.
166. **Distance-Acoustics Matching**: Attenuate volume and high frequencies as subjects recede.
167. **Audio Spectral Analysis**: Inspect spectrograms for brick-wall frequency cutoffs (e.g. 16kHz shelf).
168. **Audio Phase Consistency**: Check stereo audio for unnatural comb filtering or phase cancellation.
169. **Generated-Audio Watermark Verification**: Check audio stream against SynthID audio watermark detectors.
170. **Cross-Modal Event Matching**: Confirm visible events (thunder, glass break) produce matching audio.

### J. Scene Logic and External Fact Verification (171–185)
171. **Chronology Verification**: Compare historical clothing, vehicles, and tech to the claimed era.
172. **Location Verification**: Compare street layouts, monuments, and flora to real geographic sites.
173. **Weather Consistency**: Cross-check visible rain or snow against historical meteorological records.
174. **Event-Source Verification**: Seek independent eyewitness footage or news coverage of public events.
175. **Claimed-Person Verification**: Verify whether living individuals were physically present at the venue.
176. **Object-Existence Verification**: Confirm depicted machinery, buildings, or products exist in reality.
177. **Historical Consistency**: Audit military uniforms, signage typography, and period details.
178. **Independent Footage Comparison**: Compare footage angles against verified smartphone or press clips.
179. **Reverse-Keyframe Search**: Run Google/Yandex reverse image search on extracted keyframes.
180. **Original-Source Discovery**: Trace the earliest URL publication and creator profile.
181. **Creator-History Analysis**: Review the publisher's history for prior generative AI projects.
182. **Video-Context Preservation**: Confirm the clip was not cropped from a longer satirical or VFX reel.
183. **Source Corroboration**: Demand multiple independent streams rather than endless social reposts.
184. **Staged-vs-Synthetic Distinction**: Distinguish practical real-life stunts from digital synthesis.
185. **CGI-vs-Generative-AI Distinction**: Distinguish traditional keyframe 3D rendering from generative video.

### K. Computational Detection and Scientific Forensics (186–200)
186. **Spatial Artifact Analysis**: Model pixel co-occurrence matrices to detect neural upsampling.
187. **Frequency-Domain Analysis**: Compute 2D Fourier transforms (FFT) to locate spectral grid peaks.
188. **Wavelet Analysis**: Decompose frames into multi-scale subbands to identify high-frequency noise voids.
189. **Temporal Feature Analysis**: Use 3D convolutional networks to model inter-frame motion transitions.
190. **Optical-Flow Anomaly Scoring**: Calculate optical flow residuals to locate motion vector failures.
191. **Facial-Landmark Trajectory Analysis**: Track 68-point 3D facial landmarks for non-rigid deformation.
192. **Physiological-Signal Analysis**: Extract remote photoplethysmography (rPPG) pulses from skin capillaries.
193. **Camera-Sensor Fingerprint (PRNU)**: Check for Photo-Response Non-Uniformity sensor noise patterns.
194. **Spatiotemporal Model Classification**: Evaluate footage through validated multi-frame deepfake classifiers.
195. **Audio-Visual Model Classification**: Process dual audio and video streams through joint multimodal detectors.
196. **Multi-Detector Comparison**: Aggregate scores from diverse detector architectures before concluding.
197. **Model-Generalization Testing**: Account for detector blind spots on newer, unseen generative engines.
198. **Compression-Robustness Testing**: Evaluate how YouTube or social transcoding impacts detector confidence.
199. **False-Positive Analysis**: Measure false alarm rates on authentic low-light or heavily graded footage.
200. **Evidence-Calibrated Reporting**: State findings with calibrated uncertainty (Verified, Likely, Inconclusive).

---

## 3. Forensic Analysis Workflow on Ubuntu

For manual forensic inspection, execute these commands locally:

```bash
# 1. Inspect container metadata, streams, and encoder signatures
ffprobe -v error -show_format -show_streams -of json input.mp4 > metadata.json

# 2. Extract keyframes at 1 frame per second for reverse search and detail audit
mkdir -p /tmp/forensic_frames
ffmpeg -i input.mp4 -vf fps=1 /tmp/forensic_frames/frame_%04d.png

# 3. Create a 4x slowed review master to inspect micro-motion and temporal flicker
ffmpeg -i input.mp4 -filter:v "setpts=4*PTS" -an /tmp/forensic_slowed.mp4

# 4. Check for encoder tags or metadata traces
mediainfo input.mp4 | grep -E -i "(encoder|writing application|flow|google|veo)"
```

---

## 4. Producing Clean, Professional Master Files (Engineering Standards)

When delivering completed master edits for YouTube or production distribution, adhere to clean encoding standards:

```bash
# Re-encode to clean master with normalized metadata and no extraneous encoder comments
ffmpeg -i input.mp4 \
  -map_metadata -1 \
  -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart \
  clean_master.mp4
```

### Essential Quality Invariants
1. **Pristine Visuals**: Clean visual watermarks using localized inpainting ([remove_flow_watermark.py](../../../scripts/remove_flow_watermark.py)).
2. **Audio Compliance**: Master dialogue to -14 LUFS / -1.0 dBTP via [ffmpeg-video-editor](../ffmpeg-video-editor/SKILL.md).
3. **Disclosure Compliance**: In compliance with platform policies (YouTube Altered Content, EU AI Act), disclose synthetic generation in video descriptions or metadata flags. SynthID deep-latent watermarking is an indelible safety architecture designed by Google DeepMind and cannot and should not be stripped.
