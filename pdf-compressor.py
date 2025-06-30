#!/usr/bin/env python3
"""
PDF Compressor CLI Tool
高品質PDF圧縮ツール with 進捗表示
"""

import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path
import time
from typing import Optional, Tuple
import shutil
import getpass

class PDFCompressor:
    """PDF圧縮クラス"""
    
    # Ghostscript品質設定
    QUALITY_SETTINGS = {
        'screen': '/screen',      # 72 dpi - 最小ファイルサイズ
        'ebook': '/ebook',        # 150 dpi - 中程度品質
        'printer': '/printer',    # 300 dpi - 高品質
        'prepress': '/prepress'   # 300 dpi - 最高品質
    }
    
    def __init__(self, debug=False):
        self.ghostscript_cmd = self._find_ghostscript()
        self.debug = debug
        if not self.ghostscript_cmd:
            raise RuntimeError("Ghostscriptが見つかりません。インストールしてください。")
    
    def _find_ghostscript(self) -> Optional[str]:
        """Ghostscriptコマンドを検索"""
        for cmd in ['gs', 'ghostscript', '/usr/local/bin/gs']:
            if shutil.which(cmd):
                return cmd
        return None
    
    def _get_file_size_mb(self, filepath: str) -> float:
        """ファイルサイズをMBで取得"""
        return os.path.getsize(filepath) / (1024 * 1024)
    
    def _compress_pdf(self, input_path: str, output_path: str, quality: str, password: str = None) -> Tuple[bool, str]:
        """PDF圧縮実行"""
        cmd = [
            self.ghostscript_cmd,
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=' + self.QUALITY_SETTINGS[quality],
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            '-sOutputFile=' + output_path
        ]
        
        # パスワード付きPDFの場合
        if password:
            cmd.extend(['-sPDFPassword=' + password])
        
        cmd.append(input_path)
        
        if self.debug:
            print(f"\n[DEBUG] 実行コマンド: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if self.debug:
                print(f"[DEBUG] 戻り値: {result.returncode}")
                if result.stdout:
                    print(f"[DEBUG] stdout: {result.stdout}")
                if result.stderr:
                    print(f"[DEBUG] stderr: {result.stderr}")
            
            if result.returncode == 0:
                return True, "成功"
            else:
                error_msg = result.stderr or result.stdout or "不明なエラー"
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            return False, "タイムアウト（60秒）"
        except Exception as e:
            return False, f"実行エラー: {str(e)}"
    
    def _show_progress(self, current_step: int, total_steps: int, description: str):
        """進捗表示"""
        progress = current_step / total_steps
        bar_length = 40
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        percent = progress * 100
        
        print(f'\r進捗: [{bar}] {percent:.1f}% - {description}', end='', flush=True)
    
    def compress_to_target_size(self, input_path: str, output_path: str, 
                               target_size_mb: float, max_attempts: int = 4, password: str = None) -> Tuple[bool, str]:
        """目標サイズに向けてPDF圧縮"""
        
        if not os.path.exists(input_path):
            return False, f"入力ファイルが見つかりません: {input_path}"
        
        original_size = self._get_file_size_mb(input_path)
        print(f"📄 入力ファイル: {input_path}")
        print(f"📊 元のサイズ: {original_size:.2f} MB")
        print(f"🎯 目標サイズ: {target_size_mb:.2f} MB")
        print()
        
        if original_size <= target_size_mb:
            # 既に目標サイズ以下の場合はコピー
            shutil.copy2(input_path, output_path)
            print("✅ 既に目標サイズ以下です。ファイルをコピーしました。")
            return True, "コピー完了"
        
        # 品質レベル順（低→高品質）
        quality_order = ['screen', 'ebook', 'printer', 'prepress']
        
        best_file = None
        best_size = float('inf')
        best_quality = None
        last_error = ""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for i, quality in enumerate(quality_order):
                self._show_progress(i + 1, len(quality_order), f"品質レベル '{quality}' で圧縮中...")
                
                temp_output = os.path.join(temp_dir, f"compressed_{quality}.pdf")
                
                success, error_msg = self._compress_pdf(input_path, temp_output, quality, password)
                
                if success and os.path.exists(temp_output):
                    current_size = self._get_file_size_mb(temp_output)
                    
                    if self.debug:
                        print(f"\n[DEBUG] {quality}: {current_size:.2f} MB")
                    
                    # 目標サイズ以下で最も品質の高いものを選択
                    if current_size <= target_size_mb:
                        if best_file is None or quality_order.index(quality) > quality_order.index(best_quality):
                            if best_file and os.path.exists(best_file):
                                os.remove(best_file)
                            best_file = os.path.join(temp_dir, f"best_{quality}.pdf")
                            shutil.copy2(temp_output, best_file)
                            best_size = current_size
                            best_quality = quality
                            if self.debug:
                                print(f"[DEBUG] 新しいベスト: {quality} ({current_size:.2f} MB)")
                    
                    # 目標サイズを超えている場合、最小サイズのものを記録（フォールバック）
                    elif current_size < best_size:
                        if best_file and os.path.exists(best_file):
                            os.remove(best_file)
                        best_file = os.path.join(temp_dir, f"fallback_{quality}.pdf")
                        shutil.copy2(temp_output, best_file)
                        best_size = current_size
                        best_quality = quality
                        if self.debug:
                            print(f"[DEBUG] フォールバック更新: {quality} ({current_size:.2f} MB)")
                else:
                    last_error = error_msg
                    if self.debug:
                        print(f"\n[DEBUG] {quality} 失敗: {error_msg}")
                
                time.sleep(0.1)  # 進捗表示のため
        
        print()  # 改行
        
        if best_file and os.path.exists(best_file):
            if self.debug:
                print(f"[DEBUG] 最終選択ファイル: {best_file} (サイズ: {best_size:.2f} MB)")
            
            shutil.copy2(best_file, output_path)
            
            if best_size <= target_size_mb:
                print(f"✅ 圧縮成功!")
                print(f"📊 圧縮後サイズ: {best_size:.2f} MB")
                print(f"🎨 使用品質: {best_quality}")
                print(f"📉 圧縮率: {((original_size - best_size) / original_size * 100):.1f}%")
                return True, "圧縮成功"
            else:
                print(f"⚠️  目標サイズに到達できませんでした")
                print(f"📊 圧縮後サイズ: {best_size:.2f} MB (目標: {target_size_mb:.2f} MB)")
                print(f"🎨 使用品質: {best_quality}")
                print(f"📉 圧縮率: {((original_size - best_size) / original_size * 100):.1f}%")
                return True, "部分圧縮"
        else:
            if self.debug:
                print(f"[DEBUG] best_file が見つかりません: {best_file}")
                print(f"[DEBUG] temp_dir 内容: {os.listdir(temp_dir) if os.path.exists(temp_dir) else 'ディレクトリなし'}")
        
        # すべて失敗した場合
        error_detail = f"圧縮に失敗しました。最後のエラー: {last_error}" if last_error else "すべての品質レベルで圧縮に失敗しました"
        
        # パスワードエラーの可能性をチェック
        if "password" in last_error.lower() or "encrypted" in last_error.lower():
            return False, "パスワード付きPDFの可能性があります。-p オプションでパスワードを指定してください。"
        
        return False, error_detail

def main():
    parser = argparse.ArgumentParser(
        description='PDF圧縮ツール - 指定サイズに圧縮',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s input.pdf -s 5                    # 5MBに圧縮
  %(prog)s input.pdf -s 2.5 -o output.pdf   # 2.5MBに圧縮、出力ファイル指定
  %(prog)s input.pdf -s 10 -p               # パスワード付きPDFを10MBに圧縮
  %(prog)s input.pdf -s 5 --debug           # デバッグモードで実行
        """
    )
    
    parser.add_argument('input', help='入力PDFファイル')
    parser.add_argument('-s', '--size', type=float, required=True,
                       help='目標サイズ (MB)')
    parser.add_argument('-o', '--output', 
                       help='出力ファイル名 (デフォルト: 入力ファイル名_compressed.pdf)')
    parser.add_argument('-p', '--password', action='store_true',
                       help='パスワード付きPDF（パスワードを入力）')
    parser.add_argument('--debug', action='store_true',
                       help='デバッグモード（詳細情報を表示）')
    
    args = parser.parse_args()
    
    # パスワード取得
    password = None
    if args.password:
        password = getpass.getpass("PDFのパスワードを入力してください: ")
        if not password:
            print("❌ パスワードが入力されませんでした")
            sys.exit(1)
    
    # 出力ファイル名の設定
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input)
        output_path = str(input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}")
    
    try:
        compressor = PDFCompressor(debug=args.debug)
        success, message = compressor.compress_to_target_size(
            args.input, output_path, args.size, password=password
        )
        
        if success:
            print(f"💾 出力ファイル: {output_path}")
            print("🎉 処理完了!")
        else:
            print(f"❌ エラー: {message}")
            
            # パスワードが必要な可能性がある場合の追加ヒント
            if "パスワード" in message and not args.password:
                print("💡 ヒント: パスワード付きPDFの場合は -p オプションを使用してください")
            elif args.debug:
                print("💡 ヒント: 詳細なエラー情報は上記のDEBUG出力を確認してください")
            
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()