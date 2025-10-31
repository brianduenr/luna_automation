import sys, os, asyncio, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright
from config import LUNA_URL as DEFAULT_LUNA_URL, INPUT_CSV as DEFAULT_INPUT_CSV, OUTPUT_CSV as DEFAULT_OUTPUT_CSV, WAKE_WORD as DEFAULT_WAKE_WORD
from utils.tts_online import speak_text
from utils.stt_local import listen_and_transcribe
from utils.csv_handler import read_questions, write_header, append_result

# A default logger that just prints to the console
def default_logger(message):
    print(message)

# ========== FUNGSI PEMBANTU ==========
async def get_bot_response_text(page, logger=default_logger):
    """Mengklik tombol mode chat, lalu mengambil teks respon terakhir dari log chat."""
    chat_button_selector = "button:has(svg > path[d='M10 2c-2.236 0-4.43.18-6.57.524C1.993 2.755 1 4.014 1 5.426v5.148c0 1.413.993 2.67 2.43 2.902q1.272.206 2.57.331v3.443a.75.75 0 0 0 1.28.53l3.58-3.579a.78.78 0 0 1 .527-.224a41 41 0 0 0 5.183-.5c1.437-.232 2.43-1.49 2.43-2.903V5.426c0-1.413-.993-2.67-2.43-2.902A41 41 0 0 0 10 2m0 7a1 1 0 1 0 0-2a1 1 0 0 0 0 2M8 8a1 1 0 1 1-2 0a1 1 0 0 1 2 0m5 1a1 1 0 1 0 0-2a1 1 0 0 0 0 2'])"
    chat_text_selector = "span.whitespace-pre-line"

    try:
        logger("[🖱️] Mengklik tombol mode chat...")
        await page.click(chat_button_selector, timeout=5000)
        await page.wait_for_timeout(1000)

        logger(f"[🔍] Mencari teks di log chat dengan selector: {chat_text_selector}")
        await page.wait_for_selector(chat_text_selector, state='visible', timeout=10000)

        response_elements = await page.query_selector_all(chat_text_selector)
        if response_elements:
            last_response = response_elements[-1]
            text = await last_response.inner_text()
            logger(f"[💬] Teks ditemukan: {text}")
            return text
        else:
            logger("[⚠️] Elemen log chat tidak ditemukan setelah diklik.")
            return ""

    except Exception as e:
        logger(f"[❌] Gagal mengambil teks dari mode chat: {e}")
        return ""

async def single_test_run(page, question_data, wake_word, output_csv, logger=default_logger):
    """Menjalankan satu siklus tes untuk satu pertanyaan pada halaman yang sudah ada."""
    no = question_data["no"]
    pertanyaan = question_data["pertanyaan"]
    ekspektasi = question_data["ekspektasi_jawaban"]

    logger(f"\n[🚀] Memulai tes untuk Pertanyaan #{no}: {pertanyaan}")

    try:
        speak_text(pertanyaan)
        time.sleep(1)

        logger("[🕓] Menunggu respon audio Luna...")
        hasil_audio = listen_and_transcribe()

        logger("[🕓] Menunggu respon teks Luna...")
        hasil_teks = await get_bot_response_text(page, logger=logger)

        result = {
            "no": no, "pertanyaan": pertanyaan, "ekspektasi_jawaban": ekspektasi,
            "hasil_teks": hasil_teks, "hasil_audio": hasil_audio
        }
        append_result(output_csv, result)
        logger(f"[✅] Pertanyaan #{no} selesai.")

    except Exception as e:
        logger(f"[❌] Error pada single_test_run untuk pertanyaan #{no}: {e}")
        error_result = {
            "no": no, "pertanyaan": pertanyaan, "ekspektasi_jawaban": ekspektasi,
            "hasil_teks": f"ERROR: {e}", "hasil_audio": f"ERROR: {e}"
        }
        append_result(output_csv, error_result)


# ========== UTAMA: AUTOMATION LUNA CHATBOT ==========
async def run_automation(input_csv, output_csv, luna_url, wake_word, logger=default_logger):
    """Fungsi utama yang menjalankan keseluruhan alur tes secara asinkron."""
    questions = read_questions(input_csv)
    write_header(output_csv)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--autoplay-policy=no-user-gesture-required", "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream", "--disable-blink-features=AutomationControlled",
                "--disable-infobars", "--no-sandbox", "--start-maximized",
                "--allow-file-access-from-files", "--enable-speech-dispatcher",
            ],
        )
        context = await browser.new_context(
            permissions=["microphone", "camera"], viewport={"width": 1366, "height": 768},
        )
        page = await context.new_page()

        try:
            logger(f"[🌐] Membuka Luna: {luna_url}")
            await page.goto(luna_url)
            await page.wait_for_timeout(6000)

            await page.evaluate("() => document.querySelectorAll('video, audio').forEach(el => el.muted = false)")
            logger("✅ Autoplay audio/video diaktifkan")

            speak_text(wake_word)

            for q in questions:
                await single_test_run(page, q, wake_word, output_csv, logger=logger)

        finally:
            await context.close()
            await browser.close()
            logger(f"[🔒] Browser ditutup.")

    logger("\n[🎉] Semua pertanyaan selesai dieksekusi.")


# ========== ENTRY POINT ==========
if __name__ == "__main__":
    try:
        asyncio.run(run_automation(DEFAULT_INPUT_CSV, DEFAULT_OUTPUT_CSV, DEFAULT_LUNA_URL, DEFAULT_WAKE_WORD))
    except KeyboardInterrupt:
        print("\n🛑 Dihentikan oleh pengguna.")
