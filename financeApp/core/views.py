from django.shortcuts import render


def home(request):
    features = [
        {
            "title": "Expert Analysts",
            "description": "Seasoned finance leaders synthesize complex data into narratives executives can act on immediately.",
            "icon": "<svg viewBox='0 0 24 24' aria-hidden='true' class='h-6 w-6'><path fill='currentColor' d='M12 2a5 5 0 0 0-5 5v1.1a5 5 0 0 0-1.78 7.89l1.54 1.94a5 5 0 0 0 7.46 0l1.54-1.94A5 5 0 0 0 17 8.1V7a5 5 0 0 0-5-5Zm0 2a3 3 0 0 1 3 3v1.2a5 5 0 0 0-2.15 1.22l-1.42 1.32-1.42-1.32A5 5 0 0 0 9 8.2V7a3 3 0 0 1 3-3Zm-4.5 8a3 3 0 0 1 1.26.28l2.15 1A1 1 0 0 0 12 13a1 1 0 0 0 .09-.43l2.15-1A3 3 0 0 1 18.5 12a3 3 0 0 1-.6 1.8l-1.55 1.95a3 3 0 0 1-4.7 0l-1.55-1.95A3 3 0 0 1 7.5 12Z'/></svg>",
        },
        {
            "title": "Actionable Insights",
            "description": "Live dashboards and tailored reporting surface the KPIs that move the bottom line, not just vanity metrics.",
            "icon": "<svg viewBox='0 0 24 24' aria-hidden='true' class='h-6 w-6'><path fill='currentColor' d='M4 4a2 2 0 0 0-2 2v11.5A2.5 2.5 0 0 0 4.5 20H19a3 3 0 0 0 3-3V6a2 2 0 0 0-2-2ZM3 6a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v8.59l-3.3-3.3a1 1 0 0 0-1.4 0L13 15.59l-2.3-2.3a1 1 0 0 0-1.4 0L3 19.59Zm5.5 2A1.5 1.5 0 1 0 10 9.5 1.5 1.5 0 0 0 8.5 8Z'/></svg>",
        },
        {
            "title": "Transparent Reporting",
            "description": "Clear playbooks, frequent touchpoints, and no surprises—ever. Stakeholders stay informed at each step.",
            "icon": "<svg viewBox='0 0 24 24' aria-hidden='true' class='h-6 w-6'><path fill='currentColor' d='M6 3a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h9a2 2 0 0 0 1.41-.59l3-3A2 2 0 0 0 20 15V5a2 2 0 0 0-2-2ZM5 5a1 1 0 0 1 1-1h11a1 1 0 0 1 1 1v10h-2.5A2.5 2.5 0 0 0 13 17.5V20H6a1 1 0 0 1-1-1ZM7 6v2h8V6Zm0 4v2h6v-2Zm0 4v2h4v-2Z'/></svg>",
        },
        {
            "title": "Secure & Compliant",
            "description": "Enterprise-grade controls, SOC 2 aligned processes, and regional compliance built into every workflow.",
            "icon": "<svg viewBox='0 0 24 24' aria-hidden='true' class='h-6 w-6'><path fill='currentColor' d='M12 2a5 5 0 0 0-5 5v1.09a8 8 0 0 0-2 5.26V17a5 5 0 0 0 5 5h4a5 5 0 0 0 5-5v-3.65a8 8 0 0 0-2-5.26V7a5 5 0 0 0-5-5Zm0 2a3 3 0 0 1 3 3v1.82a8 8 0 0 0-6 0V7a3 3 0 0 1 3-3Zm0 7a6 6 0 0 1 6 6v2a3 3 0 0 1-3 3h-6a3 3 0 0 1-3-3v-2a6 6 0 0 1 6-6Zm0 3a2 2 0 0 0-2 2v1a2 2 0 0 0 4 0v-1a2 2 0 0 0-2-2Z'/></svg>",
        },
        {
            "title": "Fast Turnaround",
            "description": "Rapid discovery to delivery cycles mean you capture opportunities and mitigate risk in real time.",
            "icon": "<svg viewBox='0 0 24 24' aria-hidden='true' class='h-6 w-6'><path fill='currentColor' d='M12 3a9 9 0 1 0 5.66 16l1.68 1.68a1 1 0 0 0 1.41-1.42l-1.68-1.68A9 9 0 0 0 12 3Zm0 2a7 7 0 1 1-7 7 7 7 0 0 1 7-7Zm-1 2v4.59l-2.3 2.3a1 1 0 0 0 1.4 1.42l2.6-2.6A1 1 0 0 0 13 12V7a1 1 0 0 0-2 0Z'/></svg>",
        },
        {
            "title": "Dedicated Support",
            "description": "A senior partner stays in the loop, ensuring continuity, context, and alignment with your leadership priorities.",
            "icon": "<svg viewBox='0 0 24 24' aria-hidden='true' class='h-6 w-6'><path fill='currentColor' d='M12 2a5 5 0 1 0 5 5 5 5 0 0 0-5-5ZM6.5 14A4.5 4.5 0 0 0 2 18.5V20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-1.5A4.5 4.5 0 0 0 17.5 14Z'/></svg>",
        },
    ]
    return render(request, "home.html", {"features": features})
