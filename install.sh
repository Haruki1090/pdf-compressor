#!/bin/bash

# PDF Compressor CLI Tool - インストールスクリプト
# Usage: ./install.sh

set -e  # エラーで停止

# 色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ログ関数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Ghostscript確認
check_ghostscript() {
    log_info "Ghostscriptの確認..."
    if command -v gs >/dev/null 2>&1; then
        local version=$(gs --version 2>/dev/null || echo "不明")
        log_success "Ghostscript が見つかりました (バージョン: $version)"
        return 0
    else
        log_error "Ghostscript が見つかりません"
        echo ""
        echo "インストール方法:"
        echo "  macOS:    brew install ghostscript"
        echo "  Ubuntu:   sudo apt-get install ghostscript"
        echo "  Windows:  https://www.ghostscript.com/download/gsdnld.html"
        echo ""
        read -p "Ghostscriptをインストール後、Enterを押してください..." 
        check_ghostscript
    fi
}

# Python確認
check_python() {
    log_info "Pythonの確認..."
    if command -v python3 >/dev/null 2>&1; then
        local version=$(python3 --version 2>&1 | cut -d' ' -f2)
        log_success "Python3 が見つかりました (バージョン: $version)"
        
        # バージョン確認 (3.6以上)
        local major=$(echo $version | cut -d. -f1)
        local minor=$(echo $version | cut -d. -f2)
        if [[ $major -eq 3 && $minor -ge 6 ]] || [[ $major -gt 3 ]]; then
            return 0
        else
            log_error "Python 3.6以上が必要です (現在: $version)"
            exit 1
        fi
    else
        log_error "Python3 が見つかりません"
        exit 1
    fi
}

# ディレクトリ作成
create_directories() {
    log_info "ディレクトリの作成..."
    mkdir -p ~/.local/bin
    log_success "~/.local/bin ディレクトリを作成しました"
}

# スクリプトインストール
install_script() {
    log_info "スクリプトのインストール..."
    
    local script_path="$(pwd)/pdf-compressor.py"
    local target_path="$HOME/.local/bin/pdf-compress"
    
    if [[ ! -f "$script_path" ]]; then
        log_error "pdf-compressor.py が見つかりません"
        exit 1
    fi
    
    # シンボリックリンク作成
    ln -sf "$script_path" "$target_path"
    chmod +x "$script_path"
    chmod +x "$target_path"
    
    log_success "pdf-compress コマンドをインストールしました"
}

# PATH設定確認
check_path() {
    log_info "PATH設定の確認..."
    
    local shell_rc=""
    if [[ $SHELL == *"zsh"* ]]; then
        shell_rc="$HOME/.zshrc"
    elif [[ $SHELL == *"bash"* ]]; then
        shell_rc="$HOME/.bashrc"
    else
        log_warning "サポートされていないシェル: $SHELL"
        shell_rc="$HOME/.profile"
    fi
    
    # PATHが既に設定されているかチェック
    if echo "$PATH" | grep -q "$HOME/.local/bin"; then
        log_success "PATH は既に設定されています"
    else
        log_info "PATH設定を追加..."
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$shell_rc"
        log_success "PATH設定を $shell_rc に追加しました"
        log_warning "設定を反映するには以下を実行してください:"
        echo "  source $shell_rc"
    fi
}

# インストール確認
verify_installation() {
    log_info "インストールの確認..."
    
    # PATHを一時的に設定
    export PATH="$HOME/.local/bin:$PATH"
    
    if command -v pdf-compress >/dev/null 2>&1; then
        log_success "pdf-compress コマンドが利用可能です"
        
        # ヘルプ表示テスト
        log_info "ヘルプ表示テスト..."
        pdf-compress --help >/dev/null 2>&1 && log_success "コマンドが正常に動作します"
    else
        log_error "pdf-compress コマンドが見つかりません"
        log_info "手動でPATHを設定してください:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
}

# メイン処理
main() {
    echo "🚀 PDF Compressor CLI Tool - インストーラー"
    echo "=============================================="
    echo ""
    
    # 前提条件チェック
    check_python
    check_ghostscript
    
    echo ""
    log_info "インストールを開始します..."
    
    # インストール処理
    create_directories
    install_script
    check_path
    
    echo ""
    verify_installation
    
    echo ""
    echo "=============================================="
    log_success "🎉 インストール完了!"
    echo ""
    echo "使用方法:"
    echo "  pdf-compress input.pdf -s 5"
    echo "  pdf-compress document.pdf -s 2.5 -o output.pdf"
    echo ""
    echo "詳細はREADME.mdを参照してください"
    echo ""
    
    # シェル再読み込みの提案
    if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
        log_warning "新しいターミナルを開くか、以下を実行してPATHを更新してください:"
        if [[ $SHELL == *"zsh"* ]]; then
            echo "  source ~/.zshrc"
        elif [[ $SHELL == *"bash"* ]]; then
            echo "  source ~/.bashrc"
        else
            echo "  source ~/.profile"
        fi
    fi
}

# スクリプト実行
main "$@"