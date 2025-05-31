# SPARC (Synthetic Personal Assistant and Resource Coordinator)

SPARC is a helpful AI assistant specializing in STEM fields, designed to provide concise and accurate information and assist with various tasks through voice or text interaction. SPARC comes in two versions: a local version (`sparc_local`) that runs primarily on your machine and an online version (`sparc_online`) that utilizes cloud-based services. A separate multimodal live demo (`multimodal_live_api.py`) is also included, showcasing real-time audio and video interaction.

**Recommendation:** While both versions are available, the **`sparc_online` version is heavily recommended**. It leverages powerful cloud-based models (Google Gemini) and services (ElevenLabs TTS) that generally offer faster, higher-quality, and more reliable responses compared to the local version, which is dependent on your hardware capabilities. The online models have also been developed and refined for a longer period.

## Features

- **Dual Versions:** Choose between running SPARC locally (`sparc_local`) or using online services (`sparc_online`).
- **Real-time Interaction:** Communicate with SPARC using voice (Speech-to-Text) and receive spoken responses (Text-to-Speech).
- **Function Calling & Grounding:** SPARC can perform specific tasks by calling available functions (widgets) and use tools like Google Search to access current information.
  - Accessing system information (`system.info`)
  - Setting timers (`timer.set`)
  - Creating project folders (`project.create_folder`)
  - Opening the camera (`camera.open`)
  - Managing a To-Do list (`to_do_list.py` - _Note: Not currently integrated as a callable tool in provided main scripts_)
  - Getting weather (`get_weather`)
  - Calculating travel duration (`get_travel_duration`)
- **STEM Expertise:** Designed to assist with engineering, math, and science queries.
- **Conversational:** Engages in natural language conversation.
- **Multimodal Demo:** Includes a script (`multimodal_live_api.py`) for live interaction combining audio and video (camera/screen).

## Setup

### Prerequisites

- **Python:** Ensure you have Python installed (code uses features compatible with Python 3.11+).
- **Ollama (for `sparc_local`)**: You need Ollama installed and running to serve the local LLM. Make sure you have downloaded the model specified in `SPARC/SPARC_Local.py` (e.g., `gemma3:4b-it-q4_K_M`). Performance heavily depends on your hardware.
- **CUDA (Optional, for `sparc_local` & potentially local STT/TTS models)**: For better performance with local models, a CUDA-compatible GPU and the necessary drivers are recommended. SPARC's local components attempt to automatically detect and use the GPU if available via PyTorch.
- **Microphone and Speakers:** Required for voice interaction (STT/TTS). **Headphones are strongly recommended** to prevent echo and self-interruption.
- **API Keys (for `sparc_online` & `multimodal_live_api.py`)**: See the API Key Setup section below.
- **FFmpeg (Optional, Recommended)**: The `RealtimeSTT` or `RealtimeTTS` libraries (or their dependencies) might rely on FFmpeg for audio processing. If you encounter audio errors (like `torchaudio` warnings in logs), installing FFmpeg and ensuring it's in your system's PATH is recommended.
- **System Dependencies (e.g., `portaudio`)**: Libraries like `PyAudio` might require system-level libraries (like `portaudio` on Linux/macOS or specific drivers on Windows). Consult the documentation for `PyAudio` and `RealtimeTTS` (especially if using `CoquiEngine`) for specific OS requirements.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Nlouis38/sparc.git
    cd Mark\ II
    ```
2.  **Install Dependencies:**
    Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
    Install the required Python libraries:
    ```bash
    pip install ollama websockets pyaudio RealtimeSTT RealtimeTTS torch google-generativeai opencv-python pillow mss psutil GPUtil elevenlabs python-dotenv python-weather googlemaps # Add any other specific libraries used
    ```

## API Key Setup (Environment Variables Recommended)

Both `sparc_online` and `multimodal_live_api.py` require API keys for cloud services. It is **highly recommended** to use environment variables for security instead of hardcoding keys into the scripts.

1.  **Create a `.env` file:** In the root `sparc_v1` directory, create a file named `.env`.
2.  **Add Keys to `.env`:** Open the `.env` file and add your keys in the following format:

    ```dotenv
    # .env file
    GOOGLE_API_KEY=YOUR_GOOGLE_AI_STUDIO_KEY_HERE
    ELEVENLABS_API_KEY=YOUR_ELEVENLABS_KEY_HERE
    MAPS_API_KEY=YOUR_Maps_API_KEY_HERE
    ```

3.  **Get the Keys:**

    - **Google Generative AI (Gemini API):**
      - **Purpose:** Core LLM for `sparc_online` and `multimodal_live_api.py`.
      - **Get:** Visit [Google AI Studio](https://aistudio.google.com/), sign in, and create an API key.
    - **ElevenLabs:**
      - **Purpose:** High-quality Text-to-Speech (TTS) for `sparc_online`.
      - **Get:** Go to [ElevenLabs](https://elevenlabs.io/), log in, and find your API key in your profile/settings.
    - **Google Maps:**
      - **Purpose:** Used by the `get_travel_duration` function tool in `sparc_online`.
      - **Get:** Go to the [Google Cloud Console](https://console.cloud.google.com/), create a project (or use an existing one), enable the "Directions API", and create an API key under "Credentials".

4.  **Code Usage:** The Python scripts (`SPARC_Online.py`, `multimodal_live_api.py`, `tts_latency_test.py`) use `python-dotenv` to automatically load these variables from the `.env` file when the script starts.

    ```python
    # Example from SPARC_Online.py
    from dotenv import load_dotenv
    load_dotenv() # Loads variables from .env

    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MAPS_API_KEY = os.getenv("MAPS_API_KEY")

    # ... later use these variables ...
    self.client = genai.Client(api_key=GOOGLE_API_KEY, ...)
    # or when initializing ElevenLabsEngine/Websocket connection
    ```

## Speech-to-Text (STT) and Text-to-Speech (TTS)

SPARC uses real-time libraries for voice interaction:

- **STT (Speech-to-Text):**
  - **Library:** `RealtimeSTT` is used in both `sparc_local` and `sparc_online`.
  - **Functionality:** Captures audio from the default microphone, detects speech, and transcribes it to text using a backend model (e.g., Whisper `large-v3` specified in the configs).
- **TTS (Text-to-Speech):**
  - **Library:** `RealtimeTTS` provides the framework. Different _engines_ handle the actual synthesis:
    - **`sparc_local`:** Uses `RealtimeTTS` likely with `SystemEngine` (OS default TTS) or potentially `CoquiEngine` (local neural voice, requires setup). Quality and latency depend heavily on the chosen engine and system hardware.
    - **`sparc_online` (Recommended):** Uses `ElevenlabsEngine` via WebSockets. This typically provides very low latency and high-quality, natural-sounding voices, but requires an ElevenLabs API key and internet connection.
    - **`sparc_online_noelevenlabs`:** Uses `RealtimeTTS` with `SystemEngine`, offering an online LLM experience without needing an ElevenLabs key, but using the basic OS TTS voice.

## Running SPARC

### `sparc_local`

Uses Ollama for the LLM and local engines for STT/TTS. Performance depends significantly on your CPU/GPU and RAM.

- **LLM:** Served locally via Ollama (e.g., `gemma3:4b-it-q4_K_M`).
- **STT:** `RealtimeSTT`.
- **TTS:** `RealtimeTTS` with `SystemEngine` or `CoquiEngine`.
- **To run:**
  ```bash
  # Ensure Ollama is running with the required model pulled
  python main_local.py
  ```

### `sparc_online` (Recommended)

Uses Google Gemini (cloud) for LLM and ElevenLabs (cloud) for TTS. Requires API keys and internet. Generally faster and higher quality.

- **LLM:** Google Gemini (`gemini-2.0-flash-live-001` or similar).
- **STT:** `RealtimeSTT`.
- **TTS:** `RealtimeTTS` with `ElevenlabsEngine` via WebSockets.
- **To run:**
  ```bash
  # Make sure .env file is set up with API keys
  python main_online.py
  ```

### `sparc_online_noelevenlabs`

Uses Google Gemini (cloud) for LLM and local OS TTS. A middle ground if you want the better online LLM but don't have/want an ElevenLabs key.

- **LLM:** Google Gemini (`gemini-2.0-flash-live-001` or similar).
- **STT:** `RealtimeSTT`.
- **TTS:** `RealtimeTTS` with `SystemEngine`.
- **To run:**
  ```bash
  # Make sure .env file is set up with GOOGLE_API_KEY and MAPS_API_KEY
  python main_online_noelevenlabs.py
  ```

## Multimodal Live API Demo (`multimodal_live_api.py`)

This script demonstrates real-time, multimodal interaction using the Gemini Live API. It streams audio from your microphone and video frames (from your camera or screen) to the Gemini model and plays back the audio response.

### Setup (Multimodal Demo)

- Ensure dependencies are installed (see main Installation section).
- Ensure your `GOOGLE_API_KEY` is set in your `.env` file.
- **Use headphones!**

### Running (Multimodal Demo)

- **With Camera:**
  ```bash
  python multimodal_live_api.py --mode camera # or just python multimodal_live_api.py
  ```
- **With Screen Sharing:**
  ```bash
  python multimodal_live_api.py --mode screen
  ```
- **Audio Only:**
  ```bash
  python multimodal_live_api.py --mode none
  ```
- You can type text messages in the console while the audio/video stream is running. Type 'q' and Enter to quit.

## Usage (Main SPARC Scripts)

Once `main_local.py`, `main_online.py`, or `main_online_noelevenlabs.py` is running:

- **Voice Input:** Speak clearly into your microphone. The STT engine will detect speech and transcribe it.
- **Text Input:** If you prefer typing, type your prompt into the console when it says "Enter your message:" and press Enter.
- **Exit:** Type `exit` and press Enter.

## Widgets / Tools

SPARC (`sparc_local` and `sparc_online`) can utilize several built-in functions/tools:

- **Local Widgets (`WIDGETS/` directory):** Primarily used by `sparc_local`.
  - `camera.py`: Opens the default camera feed. (_Note: Implementation returns string, doesn't keep feed open_)
  - `project.py`: Creates project folders.
  - `system.py`: Provides system hardware information.
  - `timer.py`: Sets countdown timers.
  - `to_do_list.py`: Manages a simple to-do list. (_Not integrated_)
- **Online Tools (Gemini API):** Used by `sparc_online` versions.
  - `GoogleSearch`: Accesses Google Search for current information.
  - `get_weather`: Fetches weather using `python-weather`.
  - `get_travel_duration`: Calculates travel time using `googlemaps`.
  - `CodeExecution`: Allows Gemini to generate and potentially execute code (primarily for analysis/computation, not file system interaction).

SPARC decides when to call these based on your request and the model's understanding.

## Troubleshooting

- **Audio Issues (No Input/Output):**
  - Ensure microphone/speakers are system defaults and not muted.
  - Check `PyAudio` dependencies (`portaudio`).
  - Ensure necessary permissions are granted for microphone access.
  - Try different audio devices if available.
  - Check for `FFmpeg` if errors mention audio encoding/decoding.
- **API Key Errors (`sparc_online`, `multimodal_live_api.py`):**
  - Verify keys are correct in the `.env` file.
  - Ensure the relevant APIs (Gemini, Maps, ElevenLabs) are enabled in their respective cloud consoles.
  - Check API key quotas and billing status.
- **Library Errors:**
  - Ensure all dependencies from `Installation` are correctly installed in your active virtual environment.
  - Some libraries (e.g., `torch`, `tensorflow` used by STT/TTS backends) might have specific CPU/GPU version requirements.
- **Ollama Issues (`sparc_local`):**
  - Confirm Ollama service is running.
  - Verify the specified model (e.g., `gemma3:4b-it-q4_K_M`) is downloaded (`ollama pull model_name`) and accessible.
  - Check Ollama logs for errors.
- **TTS Issues:**
  - If using `ElevenlabsEngine`, check API key and internet connection.
  - If using `CoquiEngine`, ensure it's installed correctly and models are downloaded.
  - If using `SystemEngine`, ensure your OS's built-in TTS is functional. Latency might be higher.
- **STT Issues:**
  - Check microphone levels.
  - Ensure `RealtimeSTT` model is appropriate for your hardware (larger models need more resources).
  - Background noise can interfere. Use headphones.
