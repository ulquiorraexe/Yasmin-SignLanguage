#!/usr/bin/env python3
"""
İşaret Dili Çevirici Uygulaması
Çalıştırma Dosyası
"""

import argparse
import cProfile
import logging
import os
import pstats
import sys
import tkinter as tk
from pstats import SortKey

# Proje kök dizinini sys.path'e ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Modülleri import et
from src import setup_logging
from src.main_app import SignLanguageApp
from ui_design import AppUI  # Mevcut UI tasarımı kullanılıyor


def parse_arguments():
    """Komut satırı argümanlarını ayrıştırır.

    Returns:
        argparse.Namespace: Ayıklanmış argümanlar
    """
    parser = argparse.ArgumentParser(description="İşaret Dili Çevirici Uygulaması")
    parser.add_argument(
        "--debug", action="store_true", help="Hata ayıklama modunu etkinleştir"
    )
    parser.add_argument(
        "--log-file", help="Log dosyası yolu (varsayılan: logs/app.log)"
    )
    parser.add_argument(
        "--profile", action="store_true", help="Performans profillemesini etkinleştir"
    )

    return parser.parse_args()


def run_app():
    """Uygulamayı çalıştırır."""
    # Ana pencereyi oluştur
    root = tk.Tk()

    # Uygulamayı başlat
    app = SignLanguageApp(root, AppUI)

    # Pencereyi odağa al
    root.focus_force()

    # Ana döngüyü başlat
    root.mainloop()


def main():
    """Ana fonksiyon."""
    args = parse_arguments()

    # Log seviyesini belirle
    log_level = logging.DEBUG if args.debug else logging.INFO

    # Log dosyasını belirle
    log_file = args.log_file or "logs/app.log"

    # Loglama sistemini başlat
    setup_logging(log_level, log_file)

    logger = logging.getLogger("SignLanguageApp")
    logger.info("İşaret Dili Çevirici Uygulaması başlatılıyor...")

    try:
        if args.profile:
            # Profiling başlat
            profiler = cProfile.Profile()
            profiler.enable()

            # Uygulamayı çalıştır
            run_app()

            # Profiling sonlandır
            profiler.disable()

            # Sonuçları analiz et
            stats = pstats.Stats(profiler).sort_stats(SortKey.TIME)
            stats.dump_stats("profile_results.prof")

            # Özet göster
            print("\nPerformans Analizi Sonuçları:")
            print("=" * 50)
            stats.print_stats(20)  # En yavaş 20 fonksiyonu göster
        else:
            # Normal çalıştır
            run_app()

    except Exception as e:
        logger.critical(f"Uygulama başlatılamadı: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
