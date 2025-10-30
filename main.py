import sys, os, asyncio, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright
from config import CHROME_PATH, LUNA_URL, INPUT_CSV, OUTPUT_CSV, WAKE_WORD
from utils.tts_online import speak_text
from utils.stt_local import listen_and_transcribe
from utils.csv_handler import read_questions, write_header, append_result

# ========== FUNGSI PEMBANTU ==========
async def get_bot_response_text(page):
    """Mengklik tombol mode chat, lalu mengambil teks respon terakhir dari log chat."""
    # Selector untuk tombol mode chat, menargetkan button yang berisi SVG spesifik.
    chat_button_selector = "button:has(svg > path[d='M10 2c-2.236 0-4.43.18-6.57.524C1.993 2.755 1 4.014 1 5.426v5.148c0 1.413.993 2.67 2.43 2.902q1.272.206 2.57.331v3.443a.75.75 0 0 0 1.28.53l3.58-3.579a.78.78 0 0 1 .527-.224a41 41 0 0 0 5.183-.5c1.437-.232 2.43-1.49 2.43-2.903V5.426c0-1.413-.993-2.67-2.43-2.902A41 41 0 0 0 10 2m0 7a1 1 0 1 0 0-2a1 1 0 0 0 0 2M8 8a1 1 0 1 1-2 0a1 1 0 0 1 2 0m5 1a1 1 0 1 0 0-2a1 1 0 0 0 0 2'])"
    # Selector untuk teks di dalam log chat.
    chat_text_selector = "span.whitespace-pre-line"

    try:
        # 1. Klik tombol untuk masuk ke mode chat
        print("[🖱️] Mengklik tombol mode chat...")
        await page.click(chat_button_selector, timeout=5000)
        # Beri jeda singkat agar UI chat sempat muncul
        await page.wait_for_timeout(1000)

        # 2. Ambil teks dari log chat
        print(f"[🔍] Mencari teks di log chat dengan selector: {chat_text_selector}")
        await page.wait_for_selector(chat_text_selector, state='visible', timeout=10000)

        response_elements = await page.query_selector_all(chat_text_selector)
        if response_elements:
            # Respon terakhir adalah elemen terakhir di daftar
            last_response = response_elements[-1]
            text = await last_response.inner_text()
            print(f"[💬] Teks ditemukan: {text}")
            return text
        else:
            print("[⚠️] Elemen log chat tidak ditemukan setelah diklik.")
            return ""

    except Exception as e:
        print(f"[❌] Gagal mengambil teks dari mode chat: {e}")
        return ""

async def single_test_run(p, question_data):
    """Menjalankan satu siklus tes untuk satu pertanyaan."""
    no = question_data["no"]
    pertanyaan = question_data["pertanyaan"]
    ekspektasi = question_data["ekspektasi_jawaban"]

    print(f"\n[🚀] Memulai tes untuk Pertanyaan #{no}: {pertanyaan}")

    browser = await p.chromium.launch(
        channel="chrome", headless=False, executable_path=CHROME_PATH,
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
        print(f"[🌐] Membuka Luna: {LUNA_URL}")
        await page.goto(LUNA_URL)
        await page.wait_for_timeout(6000)

        await page.evaluate("() => document.querySelectorAll('video, audio').forEach(el => el.muted = false)")
        print("✅ Autoplay audio/video diaktifkan")

        speak_text(WAKE_WORD)
        time.sleep(1)
        speak_text(pertanyaan)

        print("[🕓] Menunggu respon audio Luna...")
        hasil_audio = listen_and_transcribe()

        print("[🕓] Menunggu respon teks Luna...")
        hasil_teks = await get_bot_response_text(page)

        result = {
            "no": no, "pertanyaan": pertanyaan, "ekspektasi_jawaban": ekspektasi,
            "hasil_teks": hasil_teks, "hasil_audio": hasil_audio
        }
        append_result(OUTPUT_CSV, result)
        print(f"[✅] Pertanyaan #{no} selesai.")

    finally:
        await context.close()
        await browser.close()
        print(f"[🔒] Browser untuk Pertanyaan #{no} ditutup.")

# ========== UTAMA: AUTOMATION LUNA CHATBOT ==========
def main():
    questions = read_questions(INPUT_CSV)
    write_header(OUTPUT_CSV)

    for q in questions:
        try:
            async def run():
                async with async_playwright() as p:
                    await single_test_run(p, q)
            asyncio.run(run())
        except Exception as e:
            print(f"[❌] Terjadi error pada pertanyaan #{q['no']}: {e}")

    print("\n[🎉] Semua pertanyaan selesai dieksekusi.")

# ========== ENTRY POINT ==========
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Dihentikan oleh pengguna.")
