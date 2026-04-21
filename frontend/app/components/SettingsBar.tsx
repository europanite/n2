import React from "react";
import { Alert, Linking, Platform, Text, TouchableOpacity, useWindowDimensions, View } from "react-native";

const REPO_URL = "https://github.com/europanite/n2";
const RAW_CONTACT_URL = (process.env.EXPO_PUBLIC_FEEDBACK_FORM_URL ?? "").trim();
const CONTACT_URL =
  RAW_CONTACT_URL.startsWith("http://") || RAW_CONTACT_URL.startsWith("https://")
    ? RAW_CONTACT_URL
    : `${REPO_URL}/issues/new`;

function resolveUrl(url: string): string {
  const s = String(url ?? "").trim();
  if (!s) return "";
  if (/^[a-z][a-z0-9+.-]*:/i.test(s) || s.startsWith("//")) return s;
  if (Platform.OS === "web" && typeof window !== "undefined") {
    return new URL(s, window.location.href).toString();
  }
  return s;
}

async function openUrl(url: string) {
  const target = resolveUrl(url);
  if (!target) return;
  try {
    if (Platform.OS === "web" && typeof window !== "undefined") {
      window.open(target, "_blank", "noopener,noreferrer");
      return;
    }
    const ok = await Linking.canOpenURL(target);
    if (!ok) throw new Error("canOpenURL returned false");
    await Linking.openURL(target);
  } catch {
    Alert.alert("Open link failed", `Could not open:\n${target}`);
  }
}

function Btn({ title, onPress }: { title: string; onPress: () => void }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={{ paddingVertical: 7, paddingHorizontal: 11, borderWidth: 1, borderRadius: 10, backgroundColor: "#fff" }}
      accessibilityRole="button"
      accessibilityLabel={title}
    >
      <Text style={{ fontWeight: "700", color: "#243a73" }}>{title}</Text>
    </TouchableOpacity>
  );
}

type Props = { title?: string };

export default function SettingsBar({ title = "UNKO N2" }: Props) {
  const { width } = useWindowDimensions();
  const isNarrow = width < 600;

  return (
    <View style={{ padding: 12, borderBottomWidth: 1, backgroundColor: "#243a73", borderColor: "#1d2f5d" }}>
      {isNarrow ? (
        <View style={{ gap: 8, padding: 6, alignItems: "center" }}>
          <Text style={{ fontSize: 30, fontWeight: "700", color: "#fff" }}>{title}</Text>
          <Text style={{ color: "#dbe6ff" }}>Daily poop sentence feed for N2 learners.</Text>
          <View style={{ flexDirection: "row", gap: 8, flexWrap: "wrap", justifyContent: "center" }}>
            <Btn title="Contact" onPress={() => openUrl(CONTACT_URL)} />
          </View>
        </View>
      ) : (
        <View style={{ position: "relative", justifyContent: "center", padding: 6, minHeight: 52 }}>
          <View style={{ flexDirection: "row", alignItems: "center", justifyContent: "flex-end" }}>
            <View style={{ flexDirection: "row", gap: 8, flexWrap: "wrap", justifyContent: "flex-end" }}>
              <Btn title="Contact" onPress={() => openUrl(CONTACT_URL)} />
            </View>
          </View>

          <View
            pointerEvents="none"
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              top: 0,
              bottom: 0,
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Text style={{ fontSize: 32, fontWeight: "700", color: "#fff" }}>{title}</Text>
            <Text style={{ color: "#dbe6ff" }}>Daily poop sentence feed for N2 learners.</Text>
          </View>
        </View>
      )}
    </View>
  );
}
