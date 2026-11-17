# Kontrol listesi: Mobil uygulama (App Store + Google Play)

Son kontrol: 2026-11-17. Kaynak: [app-stores.md](../../skills/legal-launch-audit/references/app-stores.md).

## Her uygulama için
- [ ] **Gizlilik politikası URL'si:** hem mağaza kaydında hem uygulama içinde (Ayarlar → Gizlilik).
- [ ] **Apple App Privacy etiketi** ve **Google Play Data safety formu.** SDK'lar dahil gerçek davranışla birebir aynı olmalı.
- [ ] **iOS PrivacyInfo.xcprivacy** (uygulama ve SDK'lar için).
- [ ] **İzinler:** sadece kullanılanlar olmalı. iOS'ta amaç metinleri gerçek amacı açıklamalı. Android'de hassas izin varsa beyan formu.
- [ ] **Apple yaş derecelendirmesi anketi** (4+/9+/13+/16+/18+).

## Koşullu
- [ ] **Üyelik varsa:** uygulama içinden hesap silme (Apple 5.1.1(v)). Google Play ayrıca web üzerinden silme talebi linki istiyor.
- [ ] **Reklam (AdMob) varsa:** AEA, Birleşik Krallık ve İsviçre için sertifikalı CMP (Google UMP). iOS'ta takip yapıyorsan ATT izni.
- [ ] **Uygulama içi satın alma veya abonelik varsa:** satın almadan önce fiyat, dönem, yenileme ve iptal bilgisi. "Satın alımları geri yükle" butonu. Kullanım koşulları ve gizlilik linkleri.
- [ ] **Para kazanıyorsan ve AB'de yayındaysan:** **trader statüsü** beyanı (adres, telefon ve e-posta AB'de herkese açık görünür).
- [ ] **Kullanıcı içeriği varsa:** içerik bildirme, kullanıcı engelleme, filtreleme ve iletişim bilgisi.
- [ ] **Çocuklara yönelikse:** Apple Kids / Google Families kuralları ve COPPA.
- [ ] **Firebase veya yurt dışı sunucu kullanıyorsan:** KVKK md. 9 kapsamında yurt dışı aktarım; aydınlatma metninde belirt.
- [ ] **Push ile kampanya mesajı** gönderiyorsan ayrı izin al.
- [ ] **Yapay zekâ sohbet veya görsel üretimi** varsa yapay zekâ olduğunu bildir.

## Gereksiz veya kaçın 🗑️
- Kullanılmayan izinler (konum, rehber, mikrofon), "belki lazım olur" diye eklenenler.
- Hesap gerektirmeyen özellikler için zorunlu üyelik (Apple 5.1.1(v)).
- Gizlilik politikasında kullanmadığın SDK'lar veya kullandığın bir SDK'nın eksik olması.
