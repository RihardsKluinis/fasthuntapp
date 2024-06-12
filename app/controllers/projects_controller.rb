class ProjectsController < ApplicationController
  before_action :set_project, only: %i[show edit update destroy]
  before_action :authenticate_user!, except: [:index]
  protect_from_forgery except: [:index]

  # GET /projects or /projects.json
  def index
    @projects = ProjectLaunch.paginate(page: params[:page], per_page: 20)

    filter_by_social_medias if params[:social_media_list].present?
    filter_by_dates if params[:start_date].present? || params[:end_date].present?
    filter_by_checkmark_status if params[:checkmark_status].present?
    
    @selected_social_medias = params[:social_media_list] ? params[:social_media_list].split(',') : []
    respond_to do |format|
      format.html
      format.js
    end
  end

  def show
    @project = ProjectLaunch.find(params[:id])
    @profiles = @project.profiles
    @current_user = current_user
  end

  def new
    @project = ProjectLaunch.new
  end

  def edit
  end

  def create
    @project = ProjectLaunch.new(project_params)

    respond_to do |format|
      if @project.save
        format.html { redirect_to project_url(@project), notice: "Project launch was successfully created." }
        format.json { render :show, status: :created, location: @project }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @project.errors, status: :unprocessable_entity }
      end
    end
  end

  def update
    respond_to do |format|
      if @project.update(project_params)
        format.html { redirect_to project_url(@project), notice: "Project launch was successfully updated." }
        format.json { render :show, status: :ok, location: @project }
      else
        format.html { render :edit, status: :unprocessable_entity }
        format.json { render json: @project.errors, status: :unprocessable_entity }
      end
    end
  end

  def destroy
    @project.destroy!

    respond_to do |format|
      format.html { redirect_to projects_url, notice: "Project launch was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private

  # Use callbacks to share common setup or constraints between actions.
  def set_project
    @project = ProjectLaunch.find(params[:id])
  end

  # Only allow a list of trusted parameters through.
  def project_params
    params.require(:project).permit(:name, :description, :date, :image, :website, :project_id)
  end

  def filter_by_social_medias
    social_media_columns = {
      'twitter' => 'twitter',
      'websites' => 'websites',
      'instagram' => 'instagram',
      'github' => 'github',
      'linkedin' => 'linkedin'
    }
  
    if params[:social_media_list].present?
      selected_platforms = params[:social_media_list].split(',')
      conditions = selected_platforms.map do |social_media|
        column = social_media_columns[social_media]
        ProjectLaunch.joins(:profiles).where.not(profiles: { column => [nil, ''] }).select(:id)
      end
  
      if conditions.any?
        @projects = @projects.where(id: conditions.map(&:ids).reduce(:&))
      end
    end
  end

  def filter_by_dates
    if params[:start_date].present? && params[:end_date].present?
      @projects = @projects.where(date: params[:start_date]..params[:end_date])
    elsif params[:start_date].present?
      @projects = @projects.where('date >= ?', params[:start_date])
    elsif params[:end_date].present?
      @projects = @projects.where('date <= ?', params[:end_date])
    end
  end

  def filter_by_checkmark_status
    if params[:checkmark_status] == 'true'
      @projects = @projects.joins(:project_checkmarks).distinct
    elsif params[:checkmark_status] == 'false'
      @projects = @projects.left_joins(:project_checkmarks).where(project_checkmarks: { id: nil })
    end
  end
end
