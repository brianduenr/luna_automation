@echo off
echo ================================================================
echo      SETUP PERANGKAT LOOPBACK UNTUK REKAM AUDIO SISTEM
echo ================================================================
echo Script ini akan membuka Control Panel Sound untuk mengaktifkan
echo perangkat perekam audio sistem seperti "Stereo Mix" atau
echo "CABLE Output" (dari VB-Audio Virtual Cable).
echo.
echo IKUTI LANGKAH-LANGKAH DI JENDELA YANG AKAN MUNCUL:
echo 1. Buka tab "Recording".
echo 2. Klik kanan di area kosong, lalu centang "Show Disabled Devices".
echo 3. Cari perangkat bernama "Stereo Mix" atau "CABLE Output".
echo 4. Klik kanan pada perangkat tersebut, lalu pilih "Enable".
echo 5. Klik kanan lagi, lalu pilih "Set as Default Device".
echo 6. Klik OK untuk menyimpan.
echo.
echo Jika tidak ada "Stereo Mix", Anda bisa install VB-Audio
echo Virtual Cable dari https://vb-audio.com/Cable/
echo.
pause
echo Membuka Sound Control Panel...

REM Perintah ini membuka tab "Recording" di Sound
control mmsys.cpl,,1

echo.
echo Setup selesai. Pastikan Anda sudah mengikuti langkah di atas.
pause
