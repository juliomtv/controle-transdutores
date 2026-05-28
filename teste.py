import pyautogui
import time

# ==============================
# CONFIGURAÇÕES
# ==============================

IMAGEM_REFERENCIA = "figura_correta.png"  # 👈 TROQUE AQUI quando quiser
TECLA = "space"                           # tecla que será pressionada
CONFIANCA = 0.9                           # 0.8 ~ 0.95 (quanto maior, mais exato)
INTERVALO_VERIFICACAO = 0               # segundos entre verificações
ESPERA_APOS_APERTAR = 0                 # segundos após apertar space

# ==============================
# LOOP PRINCIPAL
# ==============================

print("🔍 Monitorando a tela...")
print("➡️ Pressione CTRL + C para parar")

while True:
    try:
        # Procura a imagem na tela
        local = pyautogui.locateOnScreen(
            IMAGEM_REFERENCIA,
            confidence=CONFIANCA
        )

        if local is not None:
            print("✅ Imagem encontrada! Pressionando SPACE...")
            pyautogui.press(TECLA)
            time.sleep(ESPERA_APOS_APERTAR)
        else:
            time.sleep(INTERVALO_VERIFICACAO)

    except KeyboardInterrupt:
        print("\n🛑 Script encerrado pelo usuário.")
        break

    except Exception as e:
        print("❌ Erro:", e)
        time.sleep(1)