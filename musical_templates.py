# musical_templates.py
from template_manager import TemplateCategory, TemplateConfig


def install_musical_templates(template_manager):
    """Install all musical summary templates"""

    # Base musical template
    base_template = TemplateConfig(
        name="musical_summary_base",
        category=TemplateCategory.CUSTOM,
        system_prompt="You are a creative musical interpreter who transforms factual content into song lyrics. You maintain the key information while adapting it to musical styles. Always ensure the core message remains clear despite the creative presentation.",
        instruction="Transform the transcript summary into song lyrics that maintain factual accuracy while being entertaining",
        temperature=0.7,
        focus_topics=["key_points", "main_message", "important_details"],
        output_format="# Musical Summary\n## Original Summary\n[Brief factual summary]\n\n## Song Version\n[Genre-specific lyrics]\n\n## Performance Notes\n[Brief notes about the musical style and approach]",
        description="Transforms summaries into musical lyrics while maintaining information integrity"
    )

    # Genre-specific templates
    genre_templates = [
        TemplateConfig(
            name="hiphop_summary",
            category=TemplateCategory.CUSTOM,
            system_prompt="You are a hip-hop lyricist specialized in transforming information into sophisticated rap verses. Use modern hip-hop conventions, complex rhyme schemes, and wordplay while maintaining clarity of information. Aim for a style similar to educational rappers like Lin-Manuel Miranda's Hamilton approach - sophisticated, informative, and engaging.",
            instruction="Create a hip-hop version of the summary with complex rhyme schemes and wordplay",
            temperature=0.8,
            focus_topics=["key_points", "main_message", "flow", "rhyme_scheme"],
            output_format="# Hip-Hop Summary\n## Verse Structure\n[Verse breakdown]\n\n## Lyrics\n[Hip-hop lyrics]\n\n## Flow Notes\n[Rhythm and delivery suggestions]",
            description="Transforms summaries into hip-hop lyrics with complex rhyme schemes"
        ),
        TemplateConfig(
            name="country_summary",
            category=TemplateCategory.CUSTOM,
            system_prompt="You are a country music songwriter who excels at storytelling through music. Transform information into narrative country lyrics that maintain factual accuracy while using country music conventions like storytelling, metaphors, and relatable imagery.",
            instruction="Create a country music version of the summary with strong narrative elements",
            temperature=0.7,
            focus_topics=["key_points", "narrative_flow", "country_elements"],
            output_format="# Country Music Summary\n## Verse and Chorus Structure\n[Song structure]\n\n## Lyrics\n[Country lyrics]\n\n## Musical Style Notes\n[Style and instrumentation suggestions]",
            description="Transforms summaries into country music lyrics with strong storytelling"
        ),
        TemplateConfig(
            name="ballad_summary",
            category=TemplateCategory.CUSTOM,
            system_prompt="You are an 80s power ballad songwriter who transforms information into emotional, dramatic lyrics. Use the conventions of 80s love ballads - big emotions, power choruses, and dramatic imagery - while maintaining the factual content of the message.",
            instruction="Create an 80s-style power ballad version of the summary",
            temperature=0.8,
            focus_topics=["key_points", "emotional_elements", "ballad_structure"],
            output_format="# 80s Power Ballad Summary\n## Song Structure\n[Verse/Chorus breakdown]\n\n## Lyrics\n[Ballad lyrics]\n\n## Performance Notes\n[Style and dramatic elements]",
            description="Transforms summaries into 80s-style power ballad lyrics"
        )
    ]

    # Install templates
    template_manager.save_template(base_template)
    for template in genre_templates:
        template_manager.save_template(template)