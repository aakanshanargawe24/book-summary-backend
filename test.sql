-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- ==========================================
-- 1. AUTHORS & BOOKS (Core Domain)
-- ==========================================
CREATE TABLE authors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    biography TEXT,
    profile_image_url TEXT, -- External cloud storage link (S3/CDN)
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    author_id UUID NOT NULL REFERENCES authors(id) ON DELETE RESTRICT, -- Prevent accidental deletion of an author with books
    title VARCHAR(255) NOT NULL,
    total_pages INT NOT NULL CHECK (total_pages > 0),
    cover_image_url TEXT,
    publication_year INT CHECK (publication_year > 0),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 3. CHAPTER LEVEL
-- ==========================================
CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    chapter_number INT NOT NULL CHECK (chapter_number > 0),
    name VARCHAR(255) NOT NULL,
    start_page INT CHECK (start_page > 0),
    end_page INT CHECK (end_page >= start_page),
    
    -- LLM Extracted Semantics
    events JSONB DEFAULT '[]'::jsonb,
    plot_anchors_and_threads JSONB DEFAULT '{}'::jsonb,
    world_state_rules JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_book_chapter UNIQUE (book_id, chapter_number)
);

-- ==========================================
-- 4. SECTION LEVEL
-- ==========================================
CREATE TABLE sections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_id UUID REFERENCES chapters(id) ON DELETE SET NULL, 
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE, 
    section_number INT NOT NULL CHECK (section_number > 0),
    name VARCHAR(255),
    start_page INT CHECK (start_page > 0),
    end_page INT CHECK (end_page >= start_page),
    
    -- LLM Extracted Semantics
    characters JSONB DEFAULT '[]'::jsonb,
    character_relationships JSONB DEFAULT '[]'::jsonb,
    information_asymmetry JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_book_section UNIQUE (book_id, section_number)
);

-- ==========================================
-- 5. PARAGRAPH LEVEL (para)
-- ==========================================
CREATE TABLE paragraphs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    section_id UUID REFERENCES sections(id) ON DELETE SET NULL, 
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    
    global_sequence INT NOT NULL CHECK (global_sequence > 0), 
    start_page INT NOT NULL CHECK (start_page > 0),
    end_page INT NOT NULL CHECK (end_page >= start_page),
    raw_text TEXT NOT NULL,
    
    -- LLM Analytics
    physical_character_tracking JSONB DEFAULT '{}'::jsonb,
    mental_emotional_state JSONB DEFAULT '{}'::jsonb,
    rule_enforcement JSONB DEFAULT '{}'::jsonb,
    causal_chains JSONB DEFAULT '[]'::jsonb,
    
    -- Analytical Optimization Layer
    embedding VECTOR(1536), 
    search_vector TSVECTOR,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_book_global_seq UNIQUE (book_id, global_sequence)
);

-- ==========================================
-- 2. PIPELINE SYSTEM STATE
-- ==========================================

-- System status for the entire book asset
CREATE TABLE book_processing_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    is_processed BOOLEAN NOT NULL DEFAULT FALSE,
    last_successful_run_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_book_processing UNIQUE (book_id)
);

-- Master tracking ledger for an ongoing processing session
CREATE TABLE extraction_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL, -- 'processing', 'completed', 'failed'
    current_page INT DEFAULT 1,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE
);

-- Tracking processing states for the macro objects independently
CREATE TABLE job_components_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES extraction_jobs(id) ON DELETE CASCADE,
    layer_type VARCHAR(20) NOT NULL, -- 'paragraph', 'section', 'chapter'
    last_processed_index INT NOT NULL DEFAULT 0, -- sequence num or entity num
    status VARCHAR(50) NOT NULL, -- 'pending', 'in_progress', 'done'
    error_log TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_job_layer UNIQUE (job_id, layer_type)
);

-- ==========================================
-- REFINED SANDBOX LAYER (Strictly for Boundary Routing)
-- ==========================================

-- A. Temporary Staging for Paragraphs (Unchanged: captures text fragments and sequence)
CREATE TABLE staging_paragraph_buffers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES extraction_jobs(id) ON DELETE CASCADE,
    global_sequence INT NOT NULL CHECK (global_sequence > 0),
    start_page INT NOT NULL CHECK (start_page > 0),
    end_page INT NOT NULL CHECK (end_page >= start_page),
    buffered_text TEXT NOT NULL,
    is_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_staging_para_seq UNIQUE (job_id, global_sequence)
);

-- B. Temporary Staging for Sections (Stripped of heavy analytics, optimized for routing)
CREATE TABLE staging_section_buffers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES extraction_jobs(id) ON DELETE CASCADE,
    section_number INT NOT NULL CHECK (section_number > 0),
    name VARCHAR(255),
    start_page INT CHECK (start_page > 0),
    end_page INT CHECK (end_page >= start_page),
    associated_para_sequences INT[] DEFAULT '{}', 
    
    -- NEW: Lightweight Routing Fields to help the Python algorithm group text
    focal_characters TEXT[] DEFAULT '{}',     -- Which characters are active in this room/scene right now?
    current_location TEXT,                    -- Explicit setting (e.g., "The Courtyard", "John's Study")
    time_anchor VARCHAR(100),                  -- Localized time context (e.g., "Same night", "Next morning")
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_staging_section_num UNIQUE (job_id, section_number)
);

-- C. Temporary Staging for Chapters (Stripped of heavy analytics, optimized for routing)
CREATE TABLE staging_chapter_buffers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES extraction_jobs(id) ON DELETE CASCADE,
    chapter_number INT NOT NULL CHECK (chapter_number > 0),
    name VARCHAR(255) NOT NULL,
    start_page INT CHECK (start_page > 0),
    end_page INT CHECK (end_page >= start_page),
    
    -- NEW: Lightweight Routing Fields for macro transitions
    macro_setting TEXT,                        -- Global setting (e.g., "Winterfell", "The Spaceship")
    macro_time_leap TEXT,                      -- Did a major time-jump occur at the start? (e.g., "10 Years Later")
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_staging_chapter_num UNIQUE (job_id, chapter_number)
);