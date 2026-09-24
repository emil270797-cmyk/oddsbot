from html import escape as e


def match_title(m) -> str:
    if m.status == "live":
        return f"🔴 {m.minute}' {m.home} {m.score} {m.away}"
    return f"{m.start[11:16]} {m.home} — {m.away}"


def match_card(m, odds, flow, events, lineups) -> str:
    out = [f"<b>{e(m.home)} — {e(m.away)}</b>", e(m.league)]
    if m.status == "live":
        out.append(f"🔴 {m.minute}' · счёт {m.score}")
    if odds:
        out.append(f"\n<b>Коэффициенты</b> ({e(odds.bookmaker)}, {odds.updated_at})\n"
                   f"П1 {odds.home} · Х {odds.draw} · П2 {odds.away}")
    if flow:
        vol = f", объём {flow.volume:,.0f}" if flow.volume else ""
        out.append(f"\n<b>Прогрузы</b> ({e(flow.source)}{vol}, {flow.updated_at})\n"
                   f"П1 {flow.home_pct:.0f}% · Х {flow.draw_pct:.0f}% · П2 {flow.away_pct:.0f}%")
    if events:
        out.append("\n<b>События</b>\n" + "\n".join(
            f"{ev.minute}' {ev.type} — {e(ev.player)} ({e(ev.team)})" for ev in events))
    if lineups:
        out.append("\n<b>Составы</b>\n" + "\n".join(
            f"{e(l.team)} {l.formation or ''}: " + ", ".join(map(e, l.players)) for l in lineups))
    return "\n".join(out)


def table(rows) -> str:
    lines = [f"{r.pos}. {e(r.team)} — {r.points} оч., И {r.played}, РМ {r.goal_diff:+d}" for r in rows]
    return "<b>Таблица</b>\n" + "\n".join(lines)
