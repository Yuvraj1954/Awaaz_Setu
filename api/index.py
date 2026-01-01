/* Carousel Wrapper */
.command-carousel-wrapper {
    display: flex;
    gap: 12px;
    overflow-x: auto;
    padding: 10px 0;
    width: 100%;
    scrollbar-width: none; /* Hide scrollbar Firefox */
}
.command-carousel-wrapper::-webkit-scrollbar { display: none; } /* Hide scrollbar Chrome */

.suggest-chip {
    flex: 0 0 auto;
    background: var(--glass);
    border: 1px solid var(--border);
    padding: 10px 18px;
    border-radius: 100px;
    color: #94a3b8;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: 0.3s ease;
    white-space: nowrap;
}

.suggest-chip:hover {
    background: rgba(79, 70, 229, 0.1);
    border-color: var(--primary);
    color: white;
    transform: translateY(-2px);
}
