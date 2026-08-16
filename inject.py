with open('D:/App - Planeador Computacion/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

overlay_html = """
<!-- ACTIVATION OVERLAY -->
<div id="activation-overlay" class="fixed inset-0 bg-gray-900 bg-opacity-95 z-[9999] flex flex-col items-center justify-center hidden">
    <div class="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full text-center">
        <h2 class="text-2xl font-bold text-sepBlue mb-4">Activación Requerida</h2>
        
        <div id="trial-status" class="mb-6 text-gray-700">
            <p>Días restantes de prueba: <span id="days-remaining" class="font-bold text-sepAccent">3</span></p>
            <p class="text-sm text-gray-500 mt-2">Tu ID de equipo:</p>
            <div class="bg-gray-100 p-2 rounded text-sm font-mono mt-1 select-all" id="machine-id">CARGANDO...</div>
        </div>

        <div class="mb-6">
            <label class="block text-left text-sm font-medium text-gray-700 mb-1">Código de Activación:</label>
            <input type="text" id="activation-key" class="w-full border-gray-300 rounded-md shadow-sm focus:border-sepBlue focus:ring focus:ring-sepBlue focus:ring-opacity-50 p-2 border" placeholder="Escribe tu código aquí">
            <p id="activation-error" class="text-red-500 text-sm mt-2 hidden">Código inválido.</p>
        </div>

        <div class="flex flex-col gap-3">
            <button id="btn-activate" class="w-full bg-sepGreen text-white px-4 py-2 rounded font-semibold hover:bg-green-700 transition">Activar</button>
            <button id="btn-continue-trial" class="w-full bg-sepBlue text-white px-4 py-2 rounded font-semibold hover:bg-blue-800 transition hidden">Continuar Prueba</button>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', async () => {
        if (!window.licenseAPI) return; // Not in Electron

        const licenseInfo = await window.licenseAPI.getLicenseInfo();
        const overlay = document.getElementById('activation-overlay');
        const daysRemainingSpan = document.getElementById('days-remaining');
        const machineIdSpan = document.getElementById('machine-id');
        const btnContinue = document.getElementById('btn-continue-trial');

        if (!licenseInfo.isActivated) {
            overlay.classList.remove('hidden');
            daysRemainingSpan.textContent = licenseInfo.daysRemaining;
            machineIdSpan.textContent = licenseInfo.machineId;

            if (licenseInfo.daysRemaining > 0) {
                btnContinue.classList.remove('hidden');
            } else {
                daysRemainingSpan.classList.add('text-red-600');
            }
        }

        btnContinue.addEventListener('click', () => {
            overlay.classList.add('hidden');
        });

        document.getElementById('btn-activate').addEventListener('click', async () => {
            const key = document.getElementById('activation-key').value.trim().toUpperCase();
            const result = await window.licenseAPI.activateLicense(key);
            if (result.success) {
                alert('¡Activación exitosa! Gracias por tu compra.');
                overlay.classList.add('hidden');
            } else {
                const err = document.getElementById('activation-error');
                err.textContent = result.message;
                err.classList.remove('hidden');
            }
        });
    });
</script>
"""

content = content.replace('</body>', overlay_html + '\n</body>')
with open('D:/App - Planeador Computacion/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
