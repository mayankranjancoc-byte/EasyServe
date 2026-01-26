import re

# Read the index.html file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Checkout modal HTML to insert
checkout_modal = '''
    <!-- Checkout Modal -->
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

'''

# Check if modal already exists
if 'id="checkoutModal"' not in content:
    # Insert before Bottom Navigation comment
    content = content.replace('        <!-- Bottom Navigation -->', checkout_modal + '        <!-- Bottom Navigation -->')
    print("✓ Inserted checkout modal")
else:
    print("✓ Checkout modal already exists")

# Fix updateCheckoutTotal function
old_function = '''        function updateCheckoutTotal() {
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            const discount = parseInt(document.getElementById('discountInput').value) || 0;
            document.getElementById('checkoutTotal').textContent = `₹${subtotal - discount}`;
        }'''

new_function = '''        function updateCheckoutTotal() {
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
        }'''

if old_function in content:
    content = content.replace(old_function, new_function)
    print("✓ Updated updateCheckoutTotal function")
else:
    print("✓ Function already updated or not found")

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Done! Checkout modal added successfully.")
