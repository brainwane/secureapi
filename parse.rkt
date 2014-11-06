#lang racket

(require json)

(define (header s)
  (match s
    [(pregexp "^([^:]+):(\\d+):(\\d+)\\s+(.*)$"
              (list _ file line col desc))
     (hash 'file file 'line line 'col col 'desc desc)]
    [_ #f]))
            
(define (gather-by f? xs)
  (match xs
    [(cons x xs)
     (define run  (takef xs (negate f?)))
     (define more (dropf xs (negate f?)))
     (define fx (f? x))
     (if fx
         (cons (hash-set fx 'body (string-join run "\n")) (gather-by f? more))
         (list))]
    [(list) (list)]))

(define (parse s)
  (define xs (regexp-split "\n" s))
  (define ys (gather-by header xs))
  (write-json ys))

;; (parse (file->string "example.txt"))

(module+ main
  (parse (port->string (current-input-port))))
