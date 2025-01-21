module.export={
    apps: [
    {
      name: 'bot', // Bot nomi
      script: 'main.py', // Skript nomi
      interpreter: 'python3', // Python 3 interpreterini ishlatish
      watch: true, // Fayllarni kuzatish (skript o'zgarganda qayta ishga tushirish)
      log_file: '/path/to/logs/bot.log', // Log faylini ko'rsatish
      error_file: '/path/to/logs/error.log', // Xato logini ko'rsatish
      out_file: '/path/to/logs/output.log', // Chiqish logini ko'rsatish
      time: true, // Logda vaqtni ko'rsatish
    },
  ],
};
