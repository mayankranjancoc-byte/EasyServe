from pathlib import Path
import re
# dfsjhbfjh
#fbfgddfj
#nffrrfg
FILE_PATH = Path("index.html")

CHECKOUT_MODAL = """    <!-- Checkout Modal -->
    <div class="modal" id="checkoutModal">
        <div class="modal-content" style="max-width:400px;">
            <h2 style="font-family:'Poppins',sans-serif; margin-bottom:16px;">Complete Bill</h2>
            
            <div style="margin-bottom:16px;">
                <label style="display:block; font-weight:600; margin-bottom:8px;">Customer Name (Optional)</label>
                <input type="text" id="customerNameInput" placeholder="Walk-in Customer" 
                    style="width:100%; padding:12px; border:2px solid var(--border); border-radius:8px; font-size:15px;">
            </div>

            <div style="background:var(--bg); padding:12px; border-radius:12px; margin-bottom:16px;">
                <div style="font-weight:600; margin-bottom:8px;">Items:</div>
                <div id="checkoutCart"></div>
            </div>

            <div style="margin-bottom:16px;">
                <label style="display:block; font-weight:600; margin-bottom:8px;">Discount (₹)</label>
                <input type="number" id="discountInput" value="0" min="0" oninput="updateCheckoutTotal()"
                    style="width:100%; padding:12px; border:2px solid var(--border); border-radius:8px; font-size:15px;">
            </div>

            <div style="margin-bottom:16px;">
                <label style="display:block; font-weight:600; margin-bottom:8px;">Payment Method</label>
                <select id="paymentMethod" 
                    style="width:100%; padding:12px; border:2px solid var(--border); border-radius:8px; font-size:15px;">
                    <option value="cash">Cash</option>
                    <option value="card">Card</option>
                    <option value="upi">UPI</option>
                    <option value="pending">Pending (Mark as Unpaid)</option>
                </select>
            </div>

            <div style="background:var(--bg); padding:16px; border-radius:12px; margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span>Subtotal:</span>
                    <span id="checkoutSubtotal">₹0</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span>Discount:</span>
                    <span id="checkoutDiscount">- ₹0</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-weight:700; font-size:18px; padding-top:8px; border-top:2px dashed var(--border);">
                    <span>Total:</span>
                    <span id="checkoutTotal" style="color:var(--primary);">₹0</span>
                </div>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                <button class="btn-secondary" onclick="document.getElementById('checkoutModal').classList.remove('active')">Cancel</button>
                <button class="btn-primary" onclick="completePayment()">Complete Bill</button>
            </div>
        </div>
    </div>
"""

NEW_FUNCTION = """        function updateCheckoutTotal() {
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            const discount = parseInt(document.getElementById('discountInput')?.value) || 0;
            const total = subtotal - discount;
            
            if (document.getElementById('checkoutSubtotal')) {
                document.getElementById('checkoutSubtotal').textContent = `₹${subtotal}`;
            }
            if (document.getElementById('checkoutDiscount')) {
                document.getElementById('checkoutDiscount').textContent = `- ₹${discount}`;
            }
            document.getElementById('checkoutTotal').textContent = `₹${total}`;
        }"""


def update_html_file(path: Path) -> None:
    if not path.exists():
        print(f"Error: {path} not found.")
        return

    content = path.read_text(encoding="utf-8")
    modified = False

    # 1. Insert Checkout Modal
    if 'id="checkoutModal"' not in content:
        anchor_pattern = re.compile(r"([ \t]*<!--\s*Bottom Navigation\s*-->)")
        if anchor_pattern.search(content):
            content = anchor_pattern.sub(f"{CHECKOUT_MODAL}\n\\1", content, count=1)
            modified = True
            print("✓ Inserted checkout modal")
        else:
            print("⚠️ Anchor <!-- Bottom Navigation --> not found; modal was not inserted.")
    else:
        print("✓ Checkout modal already exists")

    # 2. Update updateCheckoutTotal function
    func_pattern = re.compile(
        r"[ \t]*function\s+updateCheckoutTotal\s*\(\)\s*\{.*?\n[ \t]*\}",
        re.DOTALL,
    )

    if func_pattern.search(content):
        # Only rewrite if it doesn't already contain the new logic
        if "checkoutSubtotal" not in content:
            content = func_pattern.sub(NEW_FUNCTION, content, count=1)
            modified = True
            print("✓ Updated updateCheckoutTotal function")
        else:
            print("✓ Function already up-to-date")
    else:
        print("⚠️ function updateCheckoutTotal() not found")

    # 3. Write changes only if needed
    if modified:
        path.write_text(content, encoding="utf-8")
        print("\n✅ File saved successfully.")
    else:
        print("\nℹ️ No modifications required.")


if __name__ == "__main__":
    update_html_file(FILE_PATH)
