import { describe,expect,it } from "vitest";
import { expiryState } from "@/lib/matching";

describe("geldigheid",()=>{it("herkent verlopen bewijs",()=>expect(expiryState(new Date("2020-01-01"),new Date("2026-01-01"))).toBe("verlopen"));it("herkent bewijs dat binnen 30 dagen verloopt",()=>expect(expiryState(new Date("2026-01-20"),new Date("2026-01-01"))).toBe("verloopt binnenkort"))});
