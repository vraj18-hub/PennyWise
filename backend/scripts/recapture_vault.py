import os
from playwright.sync_api import sync_playwright

output_dir = os.path.abspath("docs/screenshots")
frontend_dir = os.path.abspath("frontend").replace("\\", "/")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()

    page.goto(f"file:///{frontend_dir}/index.html")
    page.evaluate("() => localStorage.setItem('pennywise_token', 'test-token')")
    page.goto(f"file:///{frontend_dir}/vault.html")
    page.wait_for_timeout(800)

    page.evaluate("""() => {
        const email = document.getElementById('userEmail');
        if (email) email.textContent = 'user@pennywise.app';
        const created = document.getElementById('userCreated');
        if (created) created.textContent = 'September 30, 2026';
        const txnCount = document.getElementById('txnCount');
        if (txnCount) txnCount.textContent = 'Showing 4 transactions';
        const tableArea = document.getElementById('txnTableArea');
        if (tableArea) {
            tableArea.innerHTML = `
                <table class="txn-table">
                    <thead><tr><th>Date</th><th>Description</th><th>Category</th><th>Amount</th></tr></thead>
                    <tbody>
                        <tr><td>9/28/2026</td><td>Monthly Salary</td><td>income</td><td class="amt-pos">+$5,200.00</td></tr>
                        <tr><td>9/29/2026</td><td>Apartment Rent</td><td>housing</td><td class="amt-neg">-$1,400.00</td></tr>
                        <tr><td>9/29/2026</td><td>Whole Foods</td><td>groceries</td><td class="amt-neg">-$245.50</td></tr>
                        <tr><td>9/30/2026</td><td>Electric & Water</td><td>utilities</td><td class="amt-neg">-$120.00</td></tr>
                    </tbody>
                </table>
            `;
        }
    }""")
    page.screenshot(path=os.path.join(output_dir, "08_the_vault.png"))
    print("Recaptured 08_the_vault.png successfully")
    browser.close()
