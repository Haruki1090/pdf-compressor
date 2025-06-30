# PDF Compressor CLI Tool

高品質なPDF圧縮を行うコマンドラインツールです。指定したサイズに向けて最適な品質で圧縮し、リアルタイムで進捗を表示します。

## 🌟 特徴

- **品質維持**: Ghostscriptを使用した高品質圧縮
- **簡単操作**: コマンド一つで実行可能
- **進捗表示**: リアルタイムでエンコード進行状況を表示
- **カスタマイズ可能**: 目標サイズの調整が可能
- **スマート圧縮**: 複数の品質レベルを試行し最適解を選択

## 📋 必要条件

- Python 3.6以上
- Ghostscript (システムにインストール済み)

### Ghostscriptのインストール

**macOS (Homebrew):**
```bash
brew install ghostscript
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ghostscript
```

**Windows:**
- [Ghostscript公式サイト](https://www.ghostscript.com/download/gsdnld.html)からダウンロード

## 🚀 インストール

### 1. リポジトリをクローン
```bash
git clone https://github.com/yourusername/pdf-compressor.git
cd pdf-compressor
```

### 2. インストールスクリプトを実行
```bash
chmod +x install.sh
./install.sh
```

または手動インストール:

### 3. 手動インストール
```bash
# 実行可能ファイルを作成
ln -sf $(pwd)/pdf-compressor.py ~/.local/bin/pdf-compress
chmod +x ~/.local/bin/pdf-compress

# zshrcにパスを追加（初回のみ）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 📖 使用方法

### 基本的な使用方法

```bash
# 5MBに圧縮
pdf-compress document.pdf -s 5

# 2.5MBに圧縮、出力ファイル指定
pdf-compress document.pdf -s 2.5 -o compressed_document.pdf

# 10MBに圧縮
pdf-compress large_document.pdf -s 10
```

### コマンドオプション

```
使用法: pdf-compress <入力ファイル> -s <目標サイズMB> [オプション]

必須引数:
  input                    入力PDFファイル
  -s, --size SIZE         目標サイズ (MB)

オプション引数:
  -o, --output OUTPUT     出力ファイル名 (デフォルト: 入力ファイル名_compressed.pdf)
  -h, --help              ヘルプメッセージを表示
```

## 💡 使用例

### 例1: プレゼンテーション資料の圧縮
```bash
pdf-compress presentation.pdf -s 3
```

出力:
```
📄 入力ファイル: presentation.pdf
📊 元のサイズ: 15.30 MB
🎯 目標サイズ: 3.00 MB

進捗: [████████████████████████████████████████] 100.0% - 品質レベル 'ebook' で圧縮中...

✅ 圧縮成功!
📊 圧縮後サイズ: 2.85 MB
🎨 使用品質: ebook
📉 圧縮率: 81.4%
💾 出力ファイル: presentation_compressed.pdf
🎉 処理完了!
```

### 例2: 高品質維持での軽度圧縮
```bash
pdf-compress manual.pdf -s 8 -o manual_optimized.pdf
```

## 🔧 品質レベル

ツールは以下の品質レベルを自動的に試行し、最適なものを選択します:

1. **screen** (72 dpi) - 最小ファイルサイズ
2. **ebook** (150 dpi) - 中程度品質
3. **printer** (300 dpi) - 高品質
4. **prepress** (300 dpi) - 最高品質

## 🐛 トラブルシューティング

### Ghostscriptが見つからない場合
```
❌ エラー: Ghostscriptが見つかりません。インストールしてください。
```

**解決方法:**
1. Ghostscriptがインストールされているか確認: `gs --version`
2. インストールされていない場合、上記のインストール手順に従う
3. PATHが正しく設定されているか確認

### 目標サイズに到達できない場合
```
⚠️  目標サイズに到達できませんでした
📊 圧縮後サイズ: 5.20 MB (目標: 3.00 MB)
```

**解決方法:**
1. より小さな目標サイズを設定
2. 元のPDFに大きな画像が含まれている場合は、事前に画像圧縮を検討
3. PDFの内容によっては物理的な制限がある場合があります

## 📁 プロジェクト構造

```
pdf-compressor/
├── pdf-compressor.py    # メインスクリプト
├── setup.py            # セットアップスクリプト
├── requirements.txt    # 依存関係
├── install.sh          # インストールスクリプト
├── README.md          # このファイル
├── .gitignore         # Git無視ファイル
└── LICENSE            # ライセンス
```

## 🤝 貢献

プルリクエストや課題報告を歓迎します！

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📜 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 👨‍💻 作者

Your Name - your.email@example.com

プロジェクトリンク: https://github.com/yourusername/pdf-compressor

## 🙏 謝辞

- [Ghostscript](https://www.ghostscript.com/) - 優秀なPostScript/PDFインタープリター
- PDFコミュニティの皆様# pdf-compressor
