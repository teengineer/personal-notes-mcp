# Personal Notes MCP

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

Claude ile kişisel notlarınızı yapay zeka gücüyle yönetmek için Model Context Protocol (MCP) server'ı.

## 🎯 Özellikler

- ✍️ **Not Oluşturma** - Kolayca yeni notlar ekleyin
- 🔍 **Semantic Arama** - Doğal dil ile notlarınızda akıllı arama yapın
- 🏷️ **Etiketleme** - Notlarınızı organize edin ve kategorize edin
- 📋 **Not Listeleme** - Tüm notlarınızı görüntüleyin
- 🗑️ **Not Silme** - İstenmeyen notları kaldırın
- 💾 **Yerel Depolama** - Tüm veriler bilgisayarınızda güvenli

## 📦 Kurulum

### Gereksinimler

- Python 3.8 veya daha yüksek
- pip (Python paket yöneticisi)
- Git

### Adım 1: Repository'yi Klonlayın

```bash
git clone https://github.com/teengineer/personel-notes-mcp.git
cd personel-notes-mcp
```

### Adım 2: Virtual Environment Oluşturun (Opsiyonel ama Önerilen)

```bash
python -m venv venv

# Windows için:
venv\Scripts\activate

# macOS/Linux için:
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: MCP Server'ı Başlatın

```bash
python main.py
```

## 🚀 Claude'da Kullanma

### Konfigürasyon

Claude'da MCP'yi kullanmak için config dosyanızı düzenleyin:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

Şu satırları ekleyin:

```json
{
  "mcpServers": {
    "personel-notes": {
      "command": "python",
      "args": ["/path/to/personel-notes-mcp/main.py"]
    }
  }
}
```

`/path/to/personel-notes-mcp/` kısmını projenizin tam yoluna değiştirin.

### Claude'da Kullanım Örnekleri

Şu komutları Claude'da doğrudan yazabilirsiniz:

```
Yeni bir not oluştur: "Bugün yapılacaklar listesi"

Kişisel not ara: "python ile ilgili"

Tüm notlarımı listele

"İş" etiketli notları göster

Son not ID'sini sil
```

## 🛠️ Araçlar Referansı

### `create_note`

Yeni bir not oluşturur.

**Parametreler:**
- `content` (string, **zorunlu**) - Not metni
- `tags` (liste, opsiyonel) - Etiketler (ör: ["todo", "önemli"])

**Örnek:**

```
Yeni not oluştur:
- İçerik: "MCP proje GitHub'a yüklendi"
- Etiketler: ["proje", "github"]
```

### `semantic_search_notes`

Notlarınızda anlamsal (AI tabanlı) arama yapar.

**Parametreler:**
- `query` (string, **zorunlu**) - Arama sorgusu (doğal dil)
- `max_results` (sayı, opsiyonel) - Kaç sonuç dönsün? (varsayılan: 5)

**Örnek:**

```
"Yapay zeka" ile ilgili notları ara
Son 10 gün içinde yaptığım işleri ara
Projelerimle alakalı notları bul
```

### `list_notes`

Tüm notlarınızı listeler.

**Parametreler:**
- `tag` (string, opsiyonel) - Belirli etiketle filtrele
- `limit` (sayı, opsiyonel) - Kaç nota kadar göster (varsayılan: 20)

**Örnek:**

```
Tüm notlarımı listele
"İş" etiketli notları listele (max 10)
```

### `delete_note`

Belirtilen notu siler.

**Parametreler:**
- `note_id` (string, **zorunlu**) - Silinecek not ID'si

**Örnek:**

```
Not ID 123 numaralı notu sil
```

## 📁 Proje Yapısı

```
personel-notes-mcp/
├── main.py                 # MCP server ana dosyası
├── notes_manager.py        # Not yönetim modülü
├── semantic_search.py      # Semantic arama modülü
├── requirements.txt        # Python bağımlılıkları
├── README.md              # Bu dosya
├── LICENSE                # MIT Lisansı
└── notes/                 # Notlar klasörü (otomatik oluşturulur)
    └── notes.json         # Not veritabanı
```

## ⚙️ Konfigürasyon

### Veri Konumu Değiştirme

Ortam değişkeni kullanarak notların kaydedileceği yeri değiştirebilirsiniz:

```bash
export NOTES_DIR="/custom/path/to/notes"
python main.py
```

### Embedding Modeli

Semantic arama için kullanılan model:

```
Model: sentence-transformers/all-MiniLM-L6-v2
İlk kullanımda otomatik indirilir (~100MB)
```

## 🔧 Sorun Giderme

### "ModuleNotFoundError" hatası

Bağımlılıkları yeniden yükleyin:

```bash
pip install -r requirements.txt --upgrade
```

### Semantic arama çalışmıyor

Model dosyaları yükleniyor, ilk arama biraz yavaş olabilir. Lütfen bekleyin.

```bash
# Manuel olarak model indirin:
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Notlar kaydedilmiyor

Notlar klasörünün yazma izni olduğunu kontrol edin:

```bash
# Linux/macOS:
chmod -R 755 notes/

# Windows'ta klasöre sağ tıklayın > Properties > Security > Edit
```

### MCP Server çalışmıyor

Debug modunda çalıştırın:

```bash
python main.py --debug
```

## 📋 Sistem Gereksinimleri

| Gereksinim | Minimum | Önerilen |
|-----------|---------|----------|
| Python | 3.8 | 3.10+ |
| RAM | 2GB | 4GB+ |
| Disk | 500MB | 1GB+ |
| İnternet | İlk kurulum | - |

## 🤝 Katkıda Bulunma

Hataları raporlamak veya önerilerde bulunmak istiyorsanız:

1. [GitHub Issues](https://github.com/teengineer/personel-notes-mcp/issues) açın
2. Detaylı açıklama yazın
3. Hata mesajını ekleyin

Pull Request'ler de hoşlanır!

## ⚠️ Önemli Not

- Bu MCP **kişisel not yönetimi** için tasarlanmıştır
- Önemli verilerinizi düzenli olarak **yedekleyin**
- `notes/notes.json` dosyanız tüm notlarınızı içerir - dikkatli handleyin
- Community support sınırlıdır

## 📝 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın

Özgürce kullanabilir, değiştirebilir ve dağıtabilirsiniz.

## 📞 İletişim

- GitHub: [@teengineer](https://github.com/teengineer)
- Issues: [GitHub Issues](https://github.com/teengineer/personel-notes-mcp/issues)

---

**Sürüm:** 1.0.0  
**Son Güncelleme:** Haziran 2026  
**Status:** Aktif Geliştirme 🚀

---

## 🌟 Geliştirme Planı

- [ ] Web arayüzü
- [ ] Bulut senkronizasyonu
- [ ] İşbirliğine dayalı notlar
- [ ] Markdown desteği
- [ ] Dosya ekleme
- [ ] Backup otomasyonu

## 💡 İpucu

En iyi sonuç için notlarınıza açıklayıcı başlıklar ve etiketler ekleyin:

```
Not: "React performance optimization for large lists"
Etiketler: ["react", "performance", "javascript", "todo"]
```

Bu sayede semantic arama size daha iyi sonuçlar döner! 🎯
