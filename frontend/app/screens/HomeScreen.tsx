import React, { useCallback, useEffect, useMemo, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Image,
  Linking,
  Platform,
  RefreshControl,
  ScrollView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

type FeedItem = {
  kind?: string;
  text?: string;
  tweet?: string;
  place?: string;
  published_at?: string;
  created_at?: string;
  updated_at?: string;
  avatar_image?: string;
  image?: string;
  fixed_image?: string;
  links?: string[];
};

const FEED_URL = (process.env.EXPO_PUBLIC_FEED_URL ?? "./latest.json").trim() || "./latest.json";

function resolveUrl(url: string): string {
  const s = String(url ?? "").trim();
  if (!s) return "";
  if (/^[a-z][a-z0-9+.-]*:/i.test(s) || s.startsWith("//")) return s;
  if (Platform.OS === "web" && typeof window !== "undefined") {
    return new URL(s, window.location.href).toString();
  }
  return s;
}

function prettyDate(value?: string): string {
  if (!value) return "";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
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

async function copyText(text: string) {
  if (!text) return;
  try {
    if (Platform.OS === "web" && typeof navigator !== "undefined" && navigator.clipboard) {
      await navigator.clipboard.writeText(text);
      return;
    }
  } catch {
    // noop
  }
  Alert.alert("Copy", text);
}

export default function HomeScreen() {
  const [item, setItem] = useState<FeedItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string>("");

  const load = useCallback(async (mode: "initial" | "refresh" = "initial") => {
    if (mode === "initial") setLoading(true);
    if (mode === "refresh") setRefreshing(true);
    setError("");
    try {
      const res = await fetch(resolveUrl(FEED_URL), { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const next: FeedItem = data?.item ?? data;
      setItem(next);
    } catch (e: any) {
      setError(String(e?.message || e || "Failed to load latest.json"));
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    load("initial");
  }, [load]);

  const text = useMemo(() => {
    return String(item?.text || item?.tweet || "").trim();
  }, [item]);

  const publishedLabel = useMemo(() => {
    return prettyDate(item?.published_at || item?.created_at || item?.updated_at);
  }, [item]);

  const avatarUrl = useMemo(() => {
    return resolveUrl(item?.avatar_image || "image/avatar/normal.png");
  }, [item]);

  const linkList = useMemo(() => {
    return Array.isArray(item?.links) ? item!.links.filter(Boolean) : [];
  }, [item]);

  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: "#f3f6fb" }}
      contentContainerStyle={{ padding: 16, paddingBottom: 40 }}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={() => load("refresh")} />}
    >
      <View style={{ width: "100%", maxWidth: 980, alignSelf: "center", gap: 16 }}>
        <View
          style={{
            backgroundColor: "#ffffff",
            borderRadius: 16,
            padding: 16,
            borderWidth: 1,
            borderColor: "#d8deea",
          }}
        >
          <Text style={{ fontSize: 24, fontWeight: "700", color: "#22304a" }}>
            うんこ例文フィード
          </Text>
          <Text style={{ marginTop: 8, fontSize: 14, lineHeight: 22, color: "#52607a" }}>
            横須賀サービス風のレイアウトを流用した、単発カード中心の公開ページ。最新の1件を大きく見せる。
          </Text>
        </View>

        {loading ? (
          <View
            style={{
              backgroundColor: "#ffffff",
              borderRadius: 16,
              padding: 32,
              borderWidth: 1,
              borderColor: "#d8deea",
              alignItems: "center",
              justifyContent: "center",
              minHeight: 280,
              gap: 12,
            }}
          >
            <ActivityIndicator />
            <Text style={{ color: "#52607a" }}>Loading latest feed…</Text>
          </View>
        ) : error ? (
          <View
            style={{
              backgroundColor: "#fff4f4",
              borderRadius: 16,
              padding: 20,
              borderWidth: 1,
              borderColor: "#f2b8b5",
              gap: 12,
            }}
          >
            <Text style={{ fontSize: 18, fontWeight: "700", color: "#8a1c12" }}>Failed to load feed</Text>
            <Text style={{ color: "#8a1c12" }}>{error}</Text>
            <TouchableOpacity
              onPress={() => load("initial")}
              style={{
                alignSelf: "flex-start",
                backgroundColor: "#8a1c12",
                paddingHorizontal: 14,
                paddingVertical: 10,
                borderRadius: 10,
              }}
            >
              <Text style={{ color: "#fff", fontWeight: "700" }}>Retry</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={{ gap: 16 }}>
            <View
              style={{
                backgroundColor: "#ffffff",
                borderRadius: 18,
                borderWidth: 1,
                borderColor: "#d8deea",
                overflow: "hidden",
              }}
            >
              <View
                style={{
                  flexDirection: Platform.OS === "web" ? "row" : "column",
                  alignItems: Platform.OS === "web" ? "stretch" : "flex-start",
                }}
              >
                <View
                  style={{
                    width: Platform.OS === "web" ? 240 : "100%",
                    backgroundColor: "#eef3fb",
                    borderRightWidth: Platform.OS === "web" ? 1 : 0,
                    borderBottomWidth: Platform.OS === "web" ? 0 : 1,
                    borderColor: "#d8deea",
                    padding: 20,
                    alignItems: "center",
                    justifyContent: "center",
                    gap: 14,
                  }}
                >
                  <Image
                    source={{ uri: avatarUrl }}
                    style={{ width: 148, height: 148, borderRadius: 24, backgroundColor: "#fff" }}
                    resizeMode="contain"
                  />
                  <View style={{ alignItems: "center", gap: 6 }}>
                    <Text style={{ fontSize: 20, fontWeight: "700", color: "#22304a" }}>
                      UNKO N2
                    </Text>
                    <Text style={{ fontSize: 12, color: "#52607a" }}>
                      {item?.kind || "sentence"}
                    </Text>
                  </View>
                </View>

                <View style={{ flex: 1, padding: 22, gap: 16 }}>
                  <View style={{ gap: 8 }}>
                    <Text style={{ fontSize: 13, color: "#6a7690" }}>
                      Latest post
                    </Text>
                    <Text style={{ fontSize: 28, fontWeight: "700", lineHeight: 38, color: "#1d2940" }}>
                      {text || "No text"}
                    </Text>
                    <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 12 }}>
                      {!!item?.place && (
                        <Text style={{ fontSize: 13, color: "#52607a" }}>Place: {item.place}</Text>
                      )}
                      {!!publishedLabel && (
                        <Text style={{ fontSize: 13, color: "#52607a" }}>Updated: {publishedLabel}</Text>
                      )}
                    </View>
                  </View>

                  <View
                    style={{
                      backgroundColor: "#f7f9fc",
                      borderRadius: 14,
                      padding: 16,
                      borderWidth: 1,
                      borderColor: "#e1e6ef",
                      gap: 10,
                    }}
                  >
                    <Text style={{ fontWeight: "700", color: "#22304a" }}>About this service</Text>
                    <Text style={{ fontSize: 14, lineHeight: 22, color: "#52607a" }}>
                      うんこを必ず含むN2寄りの日本語例文を、軽いニュースカード風UIで見せる。横須賀サービスの
                      「中央タイトル + 大きい本文カード + シンプル導線」の空気をそのまま持ってくる。
                    </Text>
                  </View>

                  <View style={{ flexDirection: "row", flexWrap: "wrap", gap: 10 }}>
                    <TouchableOpacity
                      onPress={() => copyText(text)}
                      style={{
                        backgroundColor: "#243a73",
                        paddingHorizontal: 14,
                        paddingVertical: 10,
                        borderRadius: 10,
                      }}
                    >
                      <Text style={{ color: "#fff", fontWeight: "700" }}>Copy text</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                      onPress={() => load("refresh")}
                      style={{
                        backgroundColor: "#ffffff",
                        paddingHorizontal: 14,
                        paddingVertical: 10,
                        borderRadius: 10,
                        borderWidth: 1,
                        borderColor: "#b7c4dc",
                      }}
                    >
                      <Text style={{ color: "#243a73", fontWeight: "700" }}>Refresh</Text>
                    </TouchableOpacity>
                  </View>

                  {linkList.length > 0 && (
                    <View style={{ gap: 10 }}>
                      <Text style={{ fontWeight: "700", color: "#22304a" }}>Links</Text>
                      {linkList.map((link) => (
                        <TouchableOpacity key={link} onPress={() => openUrl(link)}>
                          <Text style={{ color: "#1b55b2", textDecorationLine: "underline" }}>{link}</Text>
                        </TouchableOpacity>
                      ))}
                    </View>
                  )}
                </View>
              </View>
            </View>

            <View
              style={{
                backgroundColor: "#ffffff",
                borderRadius: 16,
                padding: 16,
                borderWidth: 1,
                borderColor: "#d8deea",
                gap: 10,
              }}
            >
              <Text style={{ fontSize: 18, fontWeight: "700", color: "#22304a" }}>運用メモ</Text>
              <Text style={{ fontSize: 14, lineHeight: 22, color: "#52607a" }}>
                今は最新1件の見せ方を優先している。横須賀サービスに近づけるなら、次は feed/page_000.json を読んで
                カード一覧を下に並べるのが自然。
              </Text>
            </View>
          </View>
        )}
      </View>
    </ScrollView>
  );
}
