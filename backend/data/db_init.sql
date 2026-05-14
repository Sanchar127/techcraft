--
-- PostgreSQL database dump
--

\restrict 3EiI0v6jra5ytX0lZ0fNPNi46iliM2klVmpk5EgTdDnQslIDYpEhaFMbIqQ9L80

-- Dumped from database version 16.13 (Debian 16.13-1.pgdg13+1)
-- Dumped by pg_dump version 18.3 (Ubuntu 18.3-1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: techkraft
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO techkraft;

--
-- Name: candidates; Type: TABLE; Schema: public; Owner: techkraft
--

CREATE TABLE public.candidates (
    id character varying NOT NULL,
    name character varying,
    email character varying,
    role_applied character varying,
    status character varying,
    skills json,
    internal_notes character varying,
    ai_summary character varying,
    created_at timestamp without time zone,
    deleted_at timestamp without time zone
);


ALTER TABLE public.candidates OWNER TO techkraft;

--
-- Name: scores; Type: TABLE; Schema: public; Owner: techkraft
--

CREATE TABLE public.scores (
    id character varying NOT NULL,
    candidate_id character varying,
    reviewer_id character varying,
    category character varying,
    score integer,
    note character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.scores OWNER TO techkraft;

--
-- Name: users; Type: TABLE; Schema: public; Owner: techkraft
--

CREATE TABLE public.users (
    id character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    role character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO techkraft;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: techkraft
--

COPY public.alembic_version (version_num) FROM stdin;
c562d12fc0d2
\.


--
-- Data for Name: candidates; Type: TABLE DATA; Schema: public; Owner: techkraft
--

COPY public.candidates (id, name, email, role_applied, status, skills, internal_notes, ai_summary, created_at, deleted_at) FROM stdin;
18a38ebe-ff55-4314-bb7d-09c851915888	ram	ram@gmail.com	Backend dev	new	["python"]	\N	AI-generated summary for ram	2026-05-14 17:43:16.04528	\N
\.


--
-- Data for Name: scores; Type: TABLE DATA; Schema: public; Owner: techkraft
--

COPY public.scores (id, candidate_id, reviewer_id, category, score, note, created_at) FROM stdin;
b2a47f73-fa82-477d-aa03-e39b5402b120	18a38ebe-ff55-4314-bb7d-09c851915888	42a9e341-fdfe-435a-922c-9067477528b9	sassasd	4	test	2026-05-14 17:44:31.969924
6050bc3e-98da-4b4c-9060-f863c8c435a9	18a38ebe-ff55-4314-bb7d-09c851915888	42a9e341-fdfe-435a-922c-9067477528b9	ssdad	3	adadadasd	2026-05-14 19:13:09.735167
d1b5891b-a661-45d7-98cc-6067a4655cdf	18a38ebe-ff55-4314-bb7d-09c851915888	42a9e341-fdfe-435a-922c-9067477528b9	sda	3	dadada	2026-05-14 19:16:10.176563
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: techkraft
--

COPY public.users (id, email, password, role, created_at) FROM stdin;
6f3dc487-f2b4-4f8b-86a8-318bba1f9a8a	user1@example.com	473287f8298dba7163a897908958f7c0eae733e25d2e027992ea2edc9bed2fa8	reviewer	2026-05-14 17:39:10.505002
42a9e341-fdfe-435a-922c-9067477528b9	user@example.com	473287f8298dba7163a897908958f7c0eae733e25d2e027992ea2edc9bed2fa8	admin	2026-05-14 17:20:05.679477
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: techkraft
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: candidates candidates_pkey; Type: CONSTRAINT; Schema: public; Owner: techkraft
--

ALTER TABLE ONLY public.candidates
    ADD CONSTRAINT candidates_pkey PRIMARY KEY (id);


--
-- Name: scores scores_pkey; Type: CONSTRAINT; Schema: public; Owner: techkraft
--

ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: techkraft
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_candidates_id; Type: INDEX; Schema: public; Owner: techkraft
--

CREATE INDEX ix_candidates_id ON public.candidates USING btree (id);


--
-- Name: ix_candidates_role_applied; Type: INDEX; Schema: public; Owner: techkraft
--

CREATE INDEX ix_candidates_role_applied ON public.candidates USING btree (role_applied);


--
-- Name: ix_candidates_status; Type: INDEX; Schema: public; Owner: techkraft
--

CREATE INDEX ix_candidates_status ON public.candidates USING btree (status);


--
-- Name: ix_scores_candidate_id; Type: INDEX; Schema: public; Owner: techkraft
--

CREATE INDEX ix_scores_candidate_id ON public.scores USING btree (candidate_id);


--
-- Name: ix_scores_reviewer_id; Type: INDEX; Schema: public; Owner: techkraft
--

CREATE INDEX ix_scores_reviewer_id ON public.scores USING btree (reviewer_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: techkraft
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: techkraft
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_role; Type: INDEX; Schema: public; Owner: techkraft
--

CREATE INDEX ix_users_role ON public.users USING btree (role);


--
-- Name: scores scores_candidate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: techkraft
--

ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_candidate_id_fkey FOREIGN KEY (candidate_id) REFERENCES public.candidates(id);


--
-- Name: scores scores_reviewer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: techkraft
--

ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_reviewer_id_fkey FOREIGN KEY (reviewer_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 3EiI0v6jra5ytX0lZ0fNPNi46iliM2klVmpk5EgTdDnQslIDYpEhaFMbIqQ9L80

