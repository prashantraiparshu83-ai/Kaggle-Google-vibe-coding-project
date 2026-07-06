import http.server
import socketserver
import webbrowser
import sys

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

class SecureHTTPServer(socketserver.TCPServer):
    allow_reuse_address = True

def main():
    print("======================================================")
    print("      Starting local Education Gap AI Agent Server     ")
    print("======================================================")
    
    try:
        with SecureHTTPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}/index.html"
            print(f"\n[SUCCESS] Web application server running at: {url}")
            print("Press Ctrl+C to stop the local web server.")
            print("\nOpening web browser...")
            
            webbrowser.open(url)
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nStopping server...")
                sys.exit(0)
    except OSError as e:
        print(f"\n[ERROR] Could not start server on port {PORT}. The port might already be in use.")
        print(f"Details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
