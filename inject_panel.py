import re

with open('D:/Panel Activadores/Panel_Generadores.html', 'r', encoding='utf-8') as f:
    content = f.read()

nav_item = """
        <div class="nav-item" onclick="switchTab('tab-computo', this)">
            <i class="fa-solid fa-desktop" style="width: 20px;"></i>
            Computación
        </div>
"""

content = re.sub(r'(<div class="nav-item" onclick="switchTab\(\'tab-jlchess\'.*?</div>)', r'\1' + '\n' + nav_item, content, flags=re.DOTALL)

tab_content = """
        <!-- ========================================== -->
        <!-- TAB 5: PLANEADOR COMPUTACION               -->
        <!-- ========================================== -->
        <div id="tab-computo" class="tab-content">
            <div class="card">
                <h1 style="background: linear-gradient(to right, #0ea5e9, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Planeador Cómputo</h1>
                <p style="color: #94a3b8; margin-bottom: 25px; font-size: 0.9rem;">Activador para Planeador de Computación (1 equipo)</p>
                
                <div class="input-group">
                    <label>ID de Equipo del Cliente:</label>
                    <input type="text" id="machine_id_computo" class="code-input" placeholder="Ej. PC-1A2B-3C4D">
                </div>
                
                <button class="btn-primary" onclick="generateComputo()">🔐 GENERAR CLAVE</button>
                
                <div class="result-box" id="resultBox_computo">
                    <div class="input-group" style="margin-bottom: 10px;">
                        <label style="color: #4ade80; text-align: center;">Clave Generada:</label>
                        <input type="text" id="serial_output_computo" readonly onclick="copyText('serial_output_computo')">
                    </div>
                    <button class="btn-success" onclick="copyText('serial_output_computo')">📋 Copiar Clave</button>
                </div>
            </div>
        </div>
"""
content = content.replace('<!-- ========================================== -->\n        <!-- TAB 4: JL CHESS', tab_content + '\n        <!-- ========================================== -->\n        <!-- TAB 4: JL CHESS')

script_content = """
        // -------------------------
        // 5. Planeador Computación
        // -------------------------
        const COMPUTO_SECRET = 'PLANEADOR_COMPUTACION_2026_MASTER_SECRET_KEY';
        async function generateComputo() {
            const code = document.getElementById('machine_id_computo').value.trim().toUpperCase();
            if (!code) return alert("Ingresa un código");
            try {
                const encoder = new TextEncoder();
                const keyData = encoder.encode(COMPUTO_SECRET);
                const cryptoKey = await window.crypto.subtle.importKey('raw', keyData, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
                const signature = await window.crypto.subtle.sign('HMAC', cryptoKey, encoder.encode(code));
                
                const hashArray = Array.from(new Uint8Array(signature));
                const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
                const serial = hashHex.substring(0, 12);
                
                document.getElementById('serial_output_computo').value = serial;
                document.getElementById('resultBox_computo').classList.add('active');
            } catch (err) {
                console.error(err);
                alert("Error generando el código");
            }
        }
"""
content = content.replace('</script>', script_content + '\n    </script>')

with open('D:/Panel Activadores/Panel_Generadores.html', 'w', encoding='utf-8') as f:
    f.write(content)
