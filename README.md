  Ekran Süresi Yarışması

Streamlit ile geliştirilmiş, ekran süresi ve dijital alışkanlıklar hakkında sorular içeren bir bilgi yarışması uygulaması.

Özellikler

- Yarışmacıdan ad-soyad ve telefon numarası alma
- 5 seviyeli soru sistemi: 10, 20, 30, 40 ve 50 puan
- Her seviyeden soru havuzundan rastgele bir soru seçme
- Her soru için üç cevap seçeneği
- Yanlış cevapta puan düşürmeme
- Cevap sonrası doğru/yanlış geri bildirimi
- Yarışma tamamlama süresini ölçme
- Puan ve süreye göre ilk üç yarışmacıyı sıralama
- Yönetici panelinden yarışmacı bilgilerini görüntüleme
- CSV soru havuzu ve görsel desteği

## Kullanılan teknolojiler

- Python
- Streamlit
- SQLite
- pandas
- CSV

## Proje yapısı

```text
Pythonscreen_time_quiz/
├── app.py
├── database.py
├── questions.csv
├── images/
├── requirements.txt
├── .gitignore
└── README.md
```

`quiz.db` uygulamanın yerel veritabanıdır. Yarışmacıların telefon numaraları gibi kişisel bilgiler içerebileceğinden GitHub'a yüklenmemelidir.

## Kurulum

Python 3.10 veya daha yeni bir sürüm önerilir.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Soru dosyası: `questions.csv`

CSV dosyasında şu sütunlar bulunmalıdır:

| Sütun | Açıklama |
|---|---|
| `question_text` | Soru metni |
| `option_a` | Birinci seçenek |
| `option_b` | İkinci seçenek |
| `option_c` | Üçüncü seçenek |
| `correct_answer` | Doğru seçeneğin metni |
| `level` | Seviye: 1–5 |
| `score` | Puan: 10, 20, 30, 40 veya 50 |
| `image_path` | Görsel yolu; görsel yoksa boş bırakılabilir |

Örnek CSV:

```csv
question_text,option_a,option_b,option_c,correct_answer,level,score,image_path
"Ekran süresi neyi ifade eder?","Şarj süresini","Ekran karşısında geçirilen süreyi","İnternet hızını","Ekran karşısında geçirilen süreyi",1,10,
```

### Görsel ekleme

- Görselleri `images/` klasörüne koyun.
- `image_path` hücresine `images/ornek.webp` gibi göreli yol yazın.
- Dosya adının ve uzantısının birebir eşleştiğini kontrol edin.
- Numbers ile düzenledikten sonra dosyayı CSV formatında dışa aktarın.

### Soruları veritabanına aktarma

Uygulama soruları SQLite veritabanından okur. CSV'de değişiklik yaptıktan sonra `database.py` içindeki CSV okuyan aktarım fonksiyonunu (örneğin `import_questions_from_csv()`) bir kez çalıştırın. Fonksiyonun `pd.read_csv("questions.csv")` kullandığını doğrulayın.

Aktarım fonksiyonu eski soruları silip yeniden ekliyorsa, bunu yalnızca soru havuzunu güncellemek istediğinizde çalıştırın. Önce verilerin yedeğini alın ve aktarım satırını uygulama her başladığında otomatik çalışır durumda bırakmayın.

## Sıralama mantığı

1. Daha yüksek puan alan yarışmacı üst sıradadır.
2. Puan eşitse daha kısa sürede tamamlayan üst sıradadır.
3. Puan ve süre eşitse daha önce tamamlayan üst sıradadır.

## GitHub'a yüklemeden önce

- `quiz.db` dosyasını yüklemeyin; kişisel veriler içerebilir.
- `.venv/` klasörünü yüklemeyin.
- `questions.csv` ve `images/` klasöründeki kullanılan görselleri depoya ekleyin.
- Yönetici PIN'i kaynak kodda sabit olarak yazılıysa, herkese açık GitHub deposunda görülebilir. Dağıtımdan önce değiştirin ve mümkünse `st.secrets` gibi bir yapılandırma yöntemi kullanın.
- Gerçek telefon numaraları toplanacaksa, uygulamaya kimlerin erişebildiğini ve kişisel bilgilerin nasıl korunacağını değerlendirin.

## Dağıtım notu

Streamlit Community Cloud gibi bir platformda dağıtım için depoyu GitHub'a yükleyin ve ana dosya olarak `app.py` seçin. `requirements.txt`, `questions.csv` ve kullanılan görseller depoda bulunmalıdır.

Bulut ortamındaki yerel SQLite dosyasının yeniden başlatmalar sonrasında kalıcı kalacağı varsayılmamalıdır. Yarışmacı kayıtlarının uzun vadeli korunması gerekiyorsa kalıcı bir veritabanı kullanın.
