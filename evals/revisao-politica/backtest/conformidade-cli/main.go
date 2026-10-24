// Command conformidade-local runs the (not yet deployed) conformidade tools from the platform's Go
// package against a Neon test branch, read only, for the backtest's contender (c).
//
//	conformidade-local conceito   '{"query":"bloqueio cautelar MED","desde":"2025-03-18"}'
//	conformidade-local alteracoes '{"conceito":"MED","desde":"2025-03-18"}'
//
// The database URL comes from PRODCOPY_DATABASE_URL; the build script forces a read-only session
// (default_transaction_read_only=on) and refuses production/beta/dev hosts. Built with go build -overlay
// inside services/gateway of the platform worktree, so nothing is written to that repo.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"time"

	"github.com/letradalei/platform/services/gateway/internal/conformidade"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintln(os.Stderr, "uso: conformidade-local conceito|alteracoes '<json>'")
		os.Exit(2)
	}
	dbURL := os.Getenv("PRODCOPY_DATABASE_URL")
	if dbURL == "" {
		fmt.Fprintln(os.Stderr, "PRODCOPY_DATABASE_URL não definido")
		os.Exit(2)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()
	raw := json.RawMessage(os.Args[2])
	var (
		resp any
		err  error
	)
	switch os.Args[1] {
	case "conceito":
		resp, err = conformidade.Conceito(ctx, raw, dbURL)
	case "alteracoes":
		resp, err = conformidade.Alteracoes(ctx, raw, dbURL)
	default:
		fmt.Fprintf(os.Stderr, "ferramenta desconhecida: %s\n", os.Args[1])
		os.Exit(2)
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, "erro:", err)
		os.Exit(1)
	}
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	enc.SetEscapeHTML(false)
	_ = enc.Encode(resp)
}
