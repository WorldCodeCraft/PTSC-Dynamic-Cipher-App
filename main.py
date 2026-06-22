import time
import customtkinter as ctk


# ---------------------------------------------------
class PTSC_Cipher:
    # ---------------------------------------------------
    # 1. BAŞLANGIÇ VE AYARLAR (Constructor)
    # ---------------------------------------------------
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.alphabet = (
            "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
            "abcçdefgğhıijklmnoöprsştuüvyz"
            "0123456789 !?@#$%^&*()-=_+.,;:"
        )
        self.L = len(self.alphabet)
        self.prime = 2147483647

    # ---------------------------------------------------
    # 2. DİNAMİK TOHUM (SEED) ÜRETİMİ
    # ---------------------------------------------------
    def generate_seed(self, T_h):
        return (self.secret_key * (T_h ** 2) + 7 * T_h + 11) % self.prime

    # ---------------------------------------------------
    # 3. KİMLİK/BÜTÜNLÜK DOĞRULAYICI (Custom Hash)
    # ---------------------------------------------------
    def custom_hash(self, text, T_h):
        hash_val = self.generate_seed(T_h)
        for char in text:
            val = self.alphabet.find(char) if char in self.alphabet else ord(char)
            hash_val = (((hash_val * 33) ^ (val * T_h)) % (2 ** 32))
        return hex(hash_val)

    # ---------------------------------------------------
    # 4. ŞİFRELEME İŞLEMİ (Encryption)
    # ---------------------------------------------------
    def encrypt(self, plaintext):
        T_h = time.localtime().tm_hour
        S = self.generate_seed(T_h)
        ciphertext = ""

        for i, char in enumerate(plaintext):
            if char not in self.alphabet:
                ciphertext += char
                continue

            M_i = self.alphabet.find(char)
            k_i = (3 * (S ** 2) + 5 * (i ** 3) + 17 * i) % self.L
            C_i = (M_i + k_i) % self.L
            ciphertext += self.alphabet[C_i]

        signature = self.custom_hash(plaintext, T_h)
        return f"{ciphertext}|{signature}|{T_h}"

    # ---------------------------------------------------
    # 5. ŞİFRE ÇÖZME VE DOĞRULAMA (Decryption)
    # ---------------------------------------------------
    def decrypt(self, encrypted_payload):
        try:
            parts = encrypted_payload.split('|')
            if len(parts) != 3:
                return "HATALI FORMAT", False

            ciphertext = parts[0]
            original_signature = parts[1]
            T_h = int(parts[2])
        except:
            return "HATALI FORMAT", False

        S = self.generate_seed(T_h)
        plaintext = ""

        for i, char in enumerate(ciphertext):
            if char not in self.alphabet:
                plaintext += char
                continue

            C_i = self.alphabet.find(char)
            k_i = (3 * (S ** 2) + 5 * (i ** 3) + 17 * i) % self.L
            M_i = (C_i - k_i) % self.L
            plaintext += self.alphabet[M_i]

        new_signature = self.custom_hash(plaintext, T_h)
        return plaintext, (new_signature == original_signature)


# ---------------------------------------------------
# PROFESYONEL SİBER GÜVENLİK DASHBOARD ARAYÜZÜ
# ---------------------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class KriptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PTSC - Gelişmiş Şifreleme Modülü")
        self.geometry("1000x650")
        self.resizable(False, False)

        self.kripto = PTSC_Cipher(987654321)

        # ----------------- SOL PANEL (KONTROLLER) -----------------
        self.sol_panel = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.sol_panel.pack(side="left", fill="y", padx=0, pady=0)
        self.sol_panel.pack_propagate(False)  # Genişliğin sabit kalmasını sağlar

        self.lbl_baslik = ctk.CTkLabel(self.sol_panel, text="🛡️ PTSC KONTROL", font=ctk.CTkFont(size=22, weight="bold"))
        self.lbl_baslik.pack(pady=(30, 20))

        # SEKMELİ YAPI (Tabs) - Hocanın istediği profesyonel ayrım
        self.sekme = ctk.CTkTabview(self.sol_panel, width=280)
        self.sekme.pack(padx=20, pady=10, fill="x")

        self.sekme.add("Şifrele (Encrypt)")
        self.sekme.add("Deşifrele (Decrypt)")

        # --- ŞİFRELE SEKMESİ İÇERİĞİ ---
        self.lbl_sifrele = ctk.CTkLabel(self.sekme.tab("Şifrele (Encrypt)"), text="Şifrelenecek Metin:",
                                        text_color="gray")
        self.lbl_sifrele.pack(anchor="w", pady=(10, 5))

        self.txt_sifrele = ctk.CTkEntry(self.sekme.tab("Şifrele (Encrypt)"), height=40, font=ctk.CTkFont(size=14))
        self.txt_sifrele.pack(fill="x", pady=(0, 20))
        self.txt_sifrele.insert(0, "GİZLİ PROJE BİLGİSİ")

        self.btn_sifrele = ctk.CTkButton(self.sekme.tab("Şifrele (Encrypt)"), text="🔒 ŞİFRELE", height=45,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         command=self.sifreleme_islemi)
        self.btn_sifrele.pack(fill="x")

        # --- DEŞİFRELE SEKMESİ İÇERİĞİ ---
        self.lbl_desifrele = ctk.CTkLabel(self.sekme.tab("Deşifrele (Decrypt)"),
                                          text="Şifreli Paket (Metin|Hash|Saat):", text_color="gray")
        self.lbl_desifrele.pack(anchor="w", pady=(10, 5))

        self.txt_desifrele = ctk.CTkEntry(self.sekme.tab("Deşifrele (Decrypt)"), height=40, font=ctk.CTkFont(size=14))
        self.txt_desifrele.pack(fill="x", pady=(0, 20))

        self.btn_desifrele = ctk.CTkButton(self.sekme.tab("Deşifrele (Decrypt)"), text="🔓 DEŞİFRELE", height=45,
                                           fg_color="#b35900", hover_color="#804000",
                                           font=ctk.CTkFont(size=14, weight="bold"),
                                           command=self.desifreleme_islemi)
        self.btn_desifrele.pack(fill="x")

        # --- ORTAK BUTONLAR ---
        self.btn_temizle = ctk.CTkButton(self.sol_panel, text="🗑️ EKRANI TEMİZLE", height=40,
                                         fg_color="#4a4a4a", hover_color="#333333",
                                         font=ctk.CTkFont(size=12, weight="bold"),
                                         command=self.ekrani_temizle)
        self.btn_temizle.pack(side="bottom", fill="x", padx=20, pady=30)

        # ----------------- SAĞ PANEL (SİMÜLASYON TERMİNALİ) -----------------
        self.sag_panel = ctk.CTkFrame(self, corner_radius=0, fg_color="#0c0c0c")
        self.sag_panel.pack(side="right", fill="both", expand=True)

        self.terminal = ctk.CTkTextbox(self.sag_panel, fg_color="#050505", text_color="#00ff00",
                                       font=ctk.CTkFont(family="Consolas", size=14), wrap="word")
        self.terminal.pack(fill="both", expand=True, padx=10, pady=10)

        # RENK ETİKETLERİNİ TANIMLAMA
        self.terminal.tag_config("kirmizi", foreground="#ff3333")
        self.terminal.tag_config("mavi", foreground="#3399ff")
        self.terminal.tag_config("sari", foreground="#ffff00")

        self.log_yaz("PTSC Terminali Hazır. Sistem komutu bekleniyor...", 0)

    # Efektli Terminal Yazdırma Fonksiyonu
    def log_yaz(self, metin, bekleme=0.2, renk=None):
        if renk:
            self.terminal.insert("end", metin + "\n", renk)
        else:
            self.terminal.insert("end", metin + "\n")

        self.terminal.see("end")
        self.update()
        if bekleme > 0:
            time.sleep(bekleme)

    def ekrani_temizle(self):
        self.terminal.delete("1.0", "end")
        self.log_yaz("Ekran temizlendi. Yeni komut bekleniyor...\n", 0)

    # --- SADECE ŞİFRELEME YAPAN FONKSİYON ---
    def sifreleme_islemi(self):
        mesaj = self.txt_sifrele.get().strip()
        if not mesaj:
            self.log_yaz("\n[!] HATA: Lütfen şifrelenecek bir mesaj giriniz!", 0, "kirmizi")
            return

        self.btn_sifrele.configure(state="disabled")
        zaman = time.strftime("%H:%M:%S")

        self.log_yaz("\n" + "═" * 60, 0.1, "mavi")
        self.log_yaz("▶ [İŞLEM]: ŞİFRELEME (ENCRYPTION) BAŞLATILDI", 0.2, "mavi")
        self.log_yaz("═" * 60, 0.1, "mavi")

        self.log_yaz(f" Orijinal Metin : {mesaj}", 0.3)
        self.log_yaz(f" Zaman Damgası  : {zaman}", 0.3)
        self.log_yaz(" Algoritma çalıştırılıyor ve Hash hesaplanıyor...", 0.6)

        # Şifrele
        sifreli_veri = self.kripto.encrypt(mesaj)

        self.log_yaz("\n ✔ İŞLEM BAŞARILI! OLUŞTURULAN PAKET:", 0.3)
        self.log_yaz(f"\n >> {sifreli_veri} <<\n", 0.5, "kirmizi")
        self.log_yaz(" NOT: Veri 'Deşifrele' sekmesine otomatik kopyalandı.", 0, "sari")

        # Çıkan sonucu diğer sekmeye otomatik at (Hocaya gösteriş yapmak için güzel bir özellik)
        self.txt_desifrele.delete(0, "end")
        self.txt_desifrele.insert(0, sifreli_veri)

        self.btn_sifrele.configure(state="normal")

    # --- SADECE DEŞİFRELEME YAPAN FONKSİYON ---
    def desifreleme_islemi(self):
        paket = self.txt_desifrele.get().strip()
        if not paket:
            self.log_yaz("\n[!] HATA: Lütfen çözülecek şifreli paketi giriniz!", 0, "kirmizi")
            return

        self.btn_desifrele.configure(state="disabled")

        self.log_yaz("\n" + "═" * 60, 0.1, "sari")
        self.log_yaz("▶ [İŞLEM]: DEŞİFRELEME (DECRYPTION) BAŞLATILDI", 0.2, "sari")
        self.log_yaz("═" * 60, 0.1, "sari")

        self.log_yaz(f" Gelen Paket : {paket}", 0.4)
        self.log_yaz(" Paket analiz ediliyor... (Metin, Hash, Saat Ayrıştırılıyor)", 0.6)

        # Deşifrele
        cozulmus_mesaj, dogrulama = self.kripto.decrypt(paket)

        if cozulmus_mesaj == "HATALI FORMAT":
            self.log_yaz("\n [!] SİSTEM HATASI: Geçersiz paket formatı!", 0, "kirmizi")
            self.log_yaz("     Paket 'Metin|Hash|Saat' şeklinde olmalıdır.", 0)
            self.btn_desifrele.configure(state="normal")
            return

        self.log_yaz(f"\n Kurtarılan Mesaj: {cozulmus_mesaj}", 0.5, "mavi")
        self.log_yaz("\n --- BÜTÜNLÜK VE KİMLİK KONTROLÜ (HASH) ---", 0.3)

        if dogrulama:
            self.log_yaz(" Sistem Kararı: [ ✔ GÜVENLİ / ONAYLANDI ]", 0.3)
            self.log_yaz(" İmzalar uyuşuyor. Veri dışarıdan değiştirilmemiş.\n", 0)
        else:
            self.log_yaz(" Sistem Kararı: [ ❌ İHLAL TESPİT EDİLDİ / REDDEDİLDİ ]", 0.3, "kirmizi")
            self.log_yaz(" DİKKAT: Veri bozulmuş, müdahale edilmiş veya saat/anahtar yanlış!\n", 0, "kirmizi")

        self.btn_desifrele.configure(state="normal")


if __name__ == "__main__":
    app = KriptoApp()
    app.mainloop()