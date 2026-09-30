import os
import time
from playwright.sync_api import sync_playwright

output_dir = os.path.abspath("docs/screenshots")
os.makedirs(output_dir, exist_ok=True)

frontend_dir = os.path.abspath("frontend").replace("\\", "/")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()

    # 1. Login Page (The Gate)
    page.goto(f"file:///{frontend_dir}/index.html")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(output_dir, "01_login_gate.png"))
    print("Captured 01_login_gate.png")

    # 2. Register Page (The Gate - Register Mode)
    page.click("#toggleMode")
    page.wait_for_timeout(500)
    page.screenshot(path=os.path.join(output_dir, "02_register_gate.png"))
    print("Captured 02_register_gate.png")

    # 3. Scrolled Instructions / How it works
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(output_dir, "03_how_it_works_instructions.png"))
    print("Captured 03_how_it_works_instructions.png")

    # 4. Bank Lobby Dashboard
    page.evaluate("""() => {
        document.getElementById('gate').style.display = 'none';
        const lobby = document.getElementById('lobby');
        lobby.style.opacity = '1';
        lobby.style.pointerEvents = 'auto';
        window.scrollTo(0, 0);
    }""")
    page.wait_for_timeout(800)
    page.screenshot(path=os.path.join(output_dir, "04_lobby_dashboard.png"))
    print("Captured 04_lobby_dashboard.png")

    # Mock token for desks
    context.add_init_script("""() => {
        localStorage.setItem('pennywise_token', 'mock_token_for_display');
    }""")

    # 5. Ledger Desk
    page.goto(f"file:///{frontend_dir}/ledger.html")
    page.wait_for_timeout(1000)
    page.evaluate("""() => {
        const area = document.getElementById('summaryArea');
        if (area) {
            area.innerHTML = `
                <div class="stats">
                    <div class="stat"><div class="k">Total Income</div><div class="v pos">$5,200.00</div></div>
                    <div class="stat"><div class="k">Total Expenses</div><div class="v">$2,850.00</div></div>
                    <div class="stat"><div class="k">Savings Rate</div><div class="v pos">45.19%</div></div>
                </div>
                <div class="breakdown">
                    <h2>Expense Breakdown</h2>
                    <div class="bar-row">
                        <div class="bar-label"><span>Housing</span><span>$1,400.00</span></div>
                        <div class="bar-track"><div class="bar-fill" style="width: 49%;"></div></div>
                    </div>
                    <div class="bar-row">
                        <div class="bar-label"><span>Groceries</span><span>$650.00</span></div>
                        <div class="bar-track"><div class="bar-fill" style="width: 23%;"></div></div>
                    </div>
                    <div class="bar-row">
                        <div class="bar-label"><span>Utilities</span><span>$350.00</span></div>
                        <div class="bar-track"><div class="bar-fill" style="width: 12%;"></div></div>
                    </div>
                </div>
            `;
        }
    }""")
    page.screenshot(path=os.path.join(output_dir, "05_ledger_desk.png"))
    print("Captured 05_ledger_desk.png")

    # 6. Advisor Desk
    page.goto(f"file:///{frontend_dir}/advisor.html")
    page.wait_for_timeout(1000)
    page.evaluate("""() => {
        const log = document.getElementById('chatLog');
        if (log) {
            log.innerHTML = `
                <div class="bubble user">What is the 50/30/20 budgeting rule?</div>
                <div class="bubble assistant">The 50/30/20 rule divides your after-tax income into three buckets:<br><br>• <b>50% for Needs</b> (rent, groceries, utilities)<br>• <b>30% for Wants</b> (dining out, entertainment)<br>• <b>20% for Savings & Debt repayment</b> (emergency fund, SIP, investments)<br><br><small style="color:#8A7F6C;">Sources: budgeting_savings.txt, financial_planning.txt</small></div>
            `;
        }
    }""")
    page.screenshot(path=os.path.join(output_dir, "06_advisor_desk.png"))
    print("Captured 06_advisor_desk.png")

    # 7. Coach Desk
    page.goto(f"file:///{frontend_dir}/coach.html")
    page.wait_for_timeout(1000)
    page.evaluate("""() => {
        const banner = document.getElementById('dataBanner');
        if (banner) {
            banner.className = 'data-banner ok';
            banner.textContent = 'Using your uploaded data ($5,200 income, $2,850 expenses, 45.2% savings rate).';
        }
        const log = document.getElementById('chatLog');
        if (log) {
            log.innerHTML = `
                <div class="bubble user">How much can I safely invest monthly?</div>
                <div class="bubble assistant">Based on your monthly income ($5,200) and expenses ($2,850), you have a surplus of <b>$2,350/month</b> (a solid 45.2% savings rate).<br><br>Recommendation:<br>1. Keep <b>$1,000</b> in a liquid emergency fund until 6 months of expenses are saved ($17,100).<br>2. Allocate <b>$1,350</b> towards index funds / SIP for long-term wealth building.</div>
            `;
        }
    }""")
    page.screenshot(path=os.path.join(output_dir, "07_coach_corner.png"))
    print("Captured 07_coach_corner.png")

    # 8. The Vault
    page.goto(f"file:///{frontend_dir}/vault.html")
    page.wait_for_timeout(1000)
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
    print("Captured 08_the_vault.png")

    browser.close()

print("All screenshots captured successfully!")
